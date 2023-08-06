"""
Create screenshots from video file(s)
"""

import os
import queue

from .. import errors
from ..utils import LazyModule, daemon, fs, image, timestamp, video
from . import JobBase

import logging  # isort:skip
_log = logging.getLogger(__name__)

DEFAULT_NUMBER_OF_SCREENSHOTS = 2

natsort = LazyModule(module='natsort', namespace=globals())


class ScreenshotsJob(JobBase):
    """
    Create screenshots from video file(s)

    This job adds the following signals to the :attr:`~.JobBase.signal`
    attribute:

        ``screenshots_total``
            Emitted before screenshots are created. Registered callbacks get the
            total number of screenshots as a positional argument.
    """

    name = 'screenshots'
    label = 'Screenshots'
    cache_id = None

    def initialize(self, *, content_path, timestamps=(), count=0, from_all_videos=False):
        """
        Set internal state

        :param str content_path: Path to file or directory
        :param timestamps: Screenshot positions in the video
        :type timestamps: sequence of "[[H+:]M+:]S+" strings or seconds
        :param count: How many screenshots to make

        :param bool from_all_videos: Whether to take `count` screenshots from
            each video file beneath `content_path` or only from the first video

            See :func:`.video.find_videos` for more information.

            If `content_path` is not a directory, enabling this has no effect.

        If `timestamps` and `count` are not given, screenshot positions are
        picked at even intervals. If `count` is larger than the number of
        `timestamps`, more timestamps are added.
        """
        self._content_path = content_path
        self._screenshots_created = 0
        self._screenshots_total = -1
        self._timestamps = timestamps
        self._count = count
        self._from_all_videos = from_all_videos
        self._screenshots_process = None
        self.signal.add('screenshots_total', record=True)

    def execute(self):
        """
        Execute screenshot creation subprocess

        The subprocess also picks video file(s) and timestamps.
        """
        self._screenshots_process = daemon.DaemonProcess(
            name=self.name,
            target=_screenshots_process,
            kwargs={
                'content_path': self._content_path,
                'timestamps': self._timestamps,
                'count': self._count,
                'from_all_videos': self._from_all_videos,
                'output_dir': self.home_directory,
                'overwrite': self.ignore_cache,
            },
            info_callback=self._handle_info,
            error_callback=self._handle_error,
            finished_callback=self.finish,
        )
        self._screenshots_process.start()

    def finish(self):
        """Terminate screenshot creation subprocess and finish"""
        if self._screenshots_process:
            self._screenshots_process.stop()
        super().finish()

    def _handle_info(self, info):
        if not self.is_finished:
            if 'screenshots_total' in info:
                self._screenshots_total = info['screenshots_total']
                self.signal.emit('screenshots_total', self._screenshots_total)

            if 'screenshot_path' in info:
                self._screenshots_created += 1
                self.send(info['screenshot_path'])

    def _handle_error(self, error):
        if isinstance(error, BaseException):
            self.exception(error)
        else:
            self.error(error)

    @property
    def exit_code(self):
        """`0` if all screenshots were made, `1` otherwise, `None` if unfinished"""
        if self.is_finished:
            if self.screenshots_total < 0:
                # Job is finished but _screenshots_process() never sent us
                # timestamps. That means we're either using previously cached
                # output or the job was cancelled while _screenshots_process()
                # was still initializing.
                if self.output:
                    # If we have cached output, assume the cached number of
                    # screenshots is what the user wanted because the output of
                    # unsuccessful jobs is not cached (see
                    # JobBase._write_output_cache()).
                    return 0
                else:
                    return 1
            elif len(self.output) == self.screenshots_total:
                return 0
            else:
                return 1

    @property
    def screenshots_total(self):
        """
        Total number of screenshots to make

        .. note:: This is ``-1`` until the subprocess that creates the
                  screenshots is executed and determined the number of
                  screenshots.
        """
        return self._screenshots_total

    @property
    def screenshots_created(self):
        """Total number of screenshots made so far"""
        return self._screenshots_created


def _screenshots_process(output_queue, input_queue,
                         *, content_path, timestamps, count, from_all_videos,
                         output_dir, overwrite):
    # Find appropriate video file(s) if `content_path` is a directory
    try:
        video_files = video.find_videos(content_path)
    except errors.ContentError as e:
        output_queue.put((daemon.MsgType.error, str(e)))
    else:
        if not from_all_videos:
            # Only create screenshots from first video
            del video_files[1:]

        timestamps_map = _map_timestamps(
            video_files=video_files,
            timestamps=timestamps,
            count=count,
        )

        # Herald how many screenshots we are going to make
        screenshots_total = sum((len(ts) for ts in timestamps_map.values()))
        output_queue.put((daemon.MsgType.info, {'screenshots_total': screenshots_total}))

        try:
            _screenshot_video_files(
                output_queue, input_queue,
                timestamps_map=timestamps_map,
                output_dir=output_dir,
                overwrite=overwrite,
            )
        except SystemExit:
            # _maybe_terminate signals termination by raising SystemExit. This
            # shouldn't cause any issues as long as we actually exit here.
            pass


def _screenshot_video_files(output_queue, input_queue, *, timestamps_map, output_dir, overwrite):
    # Make all screenshots from all video files
    for video_file, timestamps in timestamps_map.items():
        _maybe_terminate(input_queue=input_queue)
        _screenshot_video_file(
            output_queue, input_queue,
            video_file=video_file,
            timestamps=timestamps,
            output_dir=output_dir,
            overwrite=overwrite,
        )


def _screenshot_video_file(output_queue, input_queue, *, video_file, timestamps, output_dir, overwrite):
    # Make all screenshots from one video file
    for ts in timestamps:
        _maybe_terminate(input_queue=input_queue)
        _make_screenshot(
            output_queue,
            video_file=video_file,
            timestamp=ts,
            output_dir=output_dir,
            overwrite=overwrite,
        )


def _make_screenshot(output_queue, *, video_file, timestamp, output_dir, overwrite):
    # Make one screenshot from one video file
    screenshot_file = os.path.join(
        output_dir,
        fs.basename(video_file) + f'.{timestamp}.png',
    )
    try:
        actual_screenshot_file = image.screenshot(
            video_file=video_file,
            screenshot_file=screenshot_file,
            timestamp=timestamp,
            overwrite=overwrite,
        )
    except errors.ScreenshotError as e:
        output_queue.put((daemon.MsgType.error, str(e)))
    else:
        output_queue.put((daemon.MsgType.info, {'screenshot_path': actual_screenshot_file}))


def _map_timestamps(*, video_files, timestamps, count):
    # Map each video_file to a sequence of timestamps
    timestamps_map = {}
    for video_file in video_files:
        timestamps_map[video_file] = _validate_timestamps(
            video_file=video_file,
            timestamps=timestamps,
            count=count,
        )
    return timestamps_map


def _validate_timestamps(*, video_file, timestamps, count):
    # Validate, normalize, deduplicate and sort timestamps

    # Stay clear of the last 10 seconds
    duration = video.duration(video_file) - 10

    timestamps_pretty = set()
    for ts in timestamps:
        ts = max(0, min(duration, timestamp.parse(ts)))
        timestamps_pretty.add(timestamp.pretty(ts))

    if not timestamps and not count:
        count = DEFAULT_NUMBER_OF_SCREENSHOTS

    # Add more timestamps if the user didn't specify enough
    if count > 0 and len(timestamps_pretty) < count:
        # Convert timestamp strings to seconds
        timestamps = sorted(timestamp.parse(ts) for ts in timestamps_pretty)

        # Fractions of video duration
        positions = [ts / duration for ts in timestamps]

        # Include start and end of video
        if 0.0 not in positions:
            positions.insert(0, 0.0)
        if 1.0 not in positions:
            positions.append(1.0)

        # Insert timestamps between the two positions with the largest distance
        while len(timestamps_pretty) < count:
            pairs = [(a, b) for a, b in zip(positions, positions[1:])]
            max_distance, pos1, pos2 = max((b - a, a, b) for a, b in pairs)
            position = ((pos2 - pos1) / 2) + pos1
            timestamps_pretty.add(timestamp.pretty(duration * position))
            positions.append(position)
            positions.sort()

    return natsort.natsorted(timestamps_pretty)


def _maybe_terminate(*, input_queue):
    try:
        typ, msg = input_queue.get_nowait()
    except queue.Empty:
        pass
    else:
        if typ == daemon.MsgType.terminate:
            raise SystemExit('Terminated')

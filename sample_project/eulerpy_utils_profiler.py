from __future__ import unicode_literals
from line_profiler import LineProfiler
import sys
import glob
import math
from EulerPy.problem import Problem
from EulerPy.problem import ProblemFile
#from EulerPy.utils import human_time
import os
import json
import textwrap
import unittest


@profile
def problem_glob(extension='.py'):
    """Returns ProblemFile objects for all valid problem files"""
    filenames = glob.glob('*[0-9][0-9][0-9]*{}'.format(extension))
    return [ProblemFile(file) for file in filenames]

# Use the resource module instead of time.clock() if possible (on Unix)
try:
    import resource

except ImportError:
    import time
    @profile
    def clock():
        """
        Under Windows, system CPU time can't be measured. Return
        time.process_time() as user time and None as system time.
        """
        # Legacy support for Python 3.2 and earlier.
        if sys.version_info < (3, 3, 0):
            return time.clock(), None

        return time.process_time(), None

else:
    @profile
    def clock():
        """
        Returns a tuple (t_user, t_system) since the start of the process.
        This is done via a call to resource.getrusage, so it avoids the
        wraparound problems in time.clock().
        """
        return resource.getrusage(resource.RUSAGE_CHILDREN)[:2]

@profile
def human_time(timespan, precision=3):
    """Formats the timespan in a human readable format"""

    if timespan >= 60.0:
        # Format time greater than one minute in a human-readable format
        # Idea from http://snipplr.com/view/5713/
        @profile
        def _format_long_time(time):
            suffixes = ('d', 'h', 'm', 's')
            lengths = (24*60*60, 60*60, 60, 1)

            for suffix, length in zip(suffixes, lengths):
                value = int(time / length)

                if value > 0:
                    time %= length
                    yield '%i%s' % (value, suffix)

                if time < 1:
                    break

        return ' '.join(_format_long_time(timespan))

    else:
        units = ['s', 'ms', 'us', 'ns']

        # Attempt to replace 'us' with 'µs' if UTF-8 encoding has been set
        if hasattr(sys.stdout, 'encoding') and sys.stdout.encoding == 'UTF-8':
            try:
                units[2] = b'\xc2\xb5s'.decode('utf-8')
            except UnicodeEncodeError:
                pass

        scale = [1.0, 1e3, 1e6, 1e9]

        if timespan > 0.0:
            # Determine scale of timespan (s = 0, ms = 1, µs = 2, ns = 3)
            order = min(-int(math.floor(math.log10(timespan)) // 3), 3)
        else:
            order = 3

        return '%.*g %s' % (precision, timespan * scale[order], units[order])

@profile
def format_time(start, end):
    """Returns string with relevant time information formatted properly"""
    try:
        cpu_usr = end[0] - start[0]
        cpu_sys = end[1] - start[1]

    except TypeError:
        # `clock()[1] == None` so subtraction results in a TypeError
        return 'Time elapsed: {}'.format(human_time(cpu_usr))

    else:
        times = (human_time(x) for x in (cpu_usr, cpu_sys, cpu_usr + cpu_sys))
        return 'Time elapsed: user: {}, sys: {}, total: {}'.format(*times)

EULER_DIR = os.path.dirname(os.path.dirname(__file__))
EULER_DATA = os.path.join(EULER_DIR, 'EulerPy', 'data')

class EulerPyUtils(unittest.TestCase):
    def test_problem_format(self):
        """
        Ensure each parsed problem only contains one problem (that one problem
        does not "bleed" into the next one due to an issue with line breaks)
        """

        # Determine largest problem in problems.txt
        problems_file = os.path.join(EULER_DATA, 'problems.txt')
        with open(problems_file) as f:
            for line in f:
                if line.startswith('Problem '):
                    largest_problem = line.split(' ')[1]

        for problem in range(1, int(largest_problem) + 1):
            problemText = Problem(problem).text

            msg = "Error encountered when parsing problem {}.".format(problem)

            self.assertFalse('========='in problemText, msg=msg)
            self.assertFalse('\n\n\n' in problemText, msg=msg)

    def test_expected_problem(self):
        """Check that problem #1 returns the correct problem text"""
        problem_one = textwrap.dedent(
            """
            If we list all the natural numbers below 10 that are multiples of 3 or 5,
            we get 3, 5, 6 and 9. The sum of these multiples is 23.

            Find the sum of all the multiples of 3 or 5 below 1000.
            """
        )

        self.assertEqual(problem_one.strip(), Problem(1).text)

    def test_filename_format(self):
        """Check that filenames are being formatted correctly"""
        self.assertEqual(Problem(1).filename(), "001.py")
        self.assertEqual(Problem(10).filename(), "010.py")
        self.assertEqual(Problem(100).filename(), "100.py")

    def test_time_format(self):
        self.assertEqual(human_time(100000), '1d 3h 46m 40s')

    def test_problem_resources(self):
        """Ensure resources in `/data` match `resources.json`"""
        resources_path = os.path.join(EULER_DATA, 'resources')

        def _resource_check(filename, seen_files):
            path = os.path.join(resources_path, filename)

            # Check that resource exists in `/data`
            self.assertTrue(os.path.isfile(path),
                '%s does not exist.' % filename)

            # Add resource to set `seen_files`
            seen_files.add(filename)

        with open(os.path.join(EULER_DATA, 'resources.json')) as f:
            resource_dict = json.load(f)

        seen_files = set()

        for item in (v for k, v in resource_dict.items()):
            if isinstance(item, list):
                for subitem in item:
                    _resource_check(subitem, seen_files)
            else:
                _resource_check(item, seen_files)

        self.assertEqual(seen_files, set(os.listdir(resources_path)))

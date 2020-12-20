# Copyright (c) 2020 Antonio Yang

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from libqtile.widget import base
import subprocess

class LockHint(base.ThreadedPollText):
    orientations = base.ORIENTATION_HORIZONTAL

    defaults = [
        ("update_interval", 1.0, "Update interval for the CapsHint widget"),
        ("captal_hint", "A", "Char display when captal"),
        ("non_captal_hint", "a", "Char display when not captal"),
        ("number_hint", "Nu", "String display when number lock on"),
        ("non_number_hint", "  ", "String display when not number lock non"),
    ]

    def __init__(self, **config):
        super().__init__(**config)
        self.add_defaults(LockHint.defaults)

    def tick(self):
        self.update(self.poll())
        return self.update_interval

    def poll(self):
        # TODO: do better with an image icon
        output = ""
        s = subprocess.check_output(
                "xset q | grep Caps",
                shell=True).decode().split()
        output += self.captal_hint if s[3] == 'on' else self.non_captal_hint
        output += self.number_hint if s[7] == 'on' else self.non_number_hint
        return output

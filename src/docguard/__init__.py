"""Backward-compatibility shim for legacy docguard imports."""

import sys

import docsentry

sys.modules[__name__] = docsentry

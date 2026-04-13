#!/usr/bin/env python
"""
Django command-line utility for administrative tasks.
"""

import os
import sys


def main() -> None:
    """
    Execute les commandes d'administration Django.

    Securite:
    - Utilise explicitement le module de settings cible.
    """
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.dev")
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()

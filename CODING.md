Coding Standards
================

* Files are in UTF-8 coding; use the following as the 2nd line in
  each python file:
      `# -*- coding: UTF-8 -*-`
* The followinig vim configuration file is used as the 3rd line in
  each python file:
      `# vim: set et ai ci sm tw=78 si sw=4 ru filetype=python fileencoding=utf-8 :`
* Indentation is done with spaces, not tabs.
* 4 spaces are used for indentation.
* I'm not to be shot for using 2 spaces as indentation (old habit...).
* Physical lines should not exceed 78 characters whenever possible.
* No whitespace at the end of lines.
* Coding is done for python3; python2 compatibility is not considered any more
  after version v0.3.
* Comments about things still needing to be done are prefixes with
      `# todo:`
  and a note in the TODO.md file is added.
* Git commit messages have a type and description of the changes.
  The changes are added to the CHANGELOG.md file.
  The following types are valid:

| type    | use | backward combatible? |
| ----    | --- | ---------------------- |
| change  | changes in defaults, behaviour etc. | if possible, but might not |
| feature | new functionality | should |
| fix     | fixing problems | strongly should |
| support | support for programmers etc, no change in functionality | must |

# todo: (to be continued...)

# PRTG-Sensor-Deleter

## Summary
Deletes sensors by name on a given PRTG instance and outputs the results
to a log file.

_Note: If you have any questions or comments you can always use GitHub
discussions, or email me at farinaanthony96@gmail.com._

#### Why
Decreases sensor count on PRTG instances (particularly crowded ones) to
increase response time and keep them organized.

## Requirements
- Python >= 3.9.2
- configparser >= 5.0.2
- pandas >= 1.2.2
- pytz >= 2021.1
- requests >= 2.25.1

## Usage
- Add any additional filtering logic to the API URLs to get specific
  sensors if desired.
    - _Make sure you configure filtering options accordingly. Available
      options for filtering can be found on the PRTG API:
      https://www.paessler.com/manuals/prtg/live_multiple_object_property_status#advanced_filtering_

- Add additional logic to include more than just one sensor name to delete.

- Edit the config.ini file with relevant PRTG access information and the
  timezone for the log file naming.

- Simply run the script using Python:
  `python PRTG-Sensor-Deleter.py`

## Compatibility
Should be able to run on any machine with a Python interpreter. This script
was only tested on a Windows machine running Python 3.9.2.

## Disclaimer
The code provided in this project is an open source example and should not
be treated as an officially supported product. Use at your own risk. If you
encounter any problems, please log an
[issue](https://github.com/CC-Digital-Innovation/PRTG-Sensor-Deleter/issues).

## Contributing
1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request ツ

## History
-  version 1.0.4 - 2021/06/08
    - Added support for multiple config files
    - Updated README.md


-  version 1.0.3 - 2021/05/19
    - Made logs go into their own directory
    

-  version 1.0.2 - 2021/05/17
    - Adjusted README.md
    - Made relative path for config.ini


-  version 1.0.1 - 2021/04/08
    - Fixed logging file name bug
    - No longer needs to generate sensor flatfile


-  version 1.0.0 - 2021/04/08
    - Initial release

## Credits
Anthony Farina <<farinaanthony96@gmail.com>>

## License
MIT License

Copyright (c) [2021] [Anthony G. Farina]

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
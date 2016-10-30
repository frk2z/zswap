#!/usr/bin/env python
import sys
import re  # regex


default_options = {'override': False, 'output': True, 'errors': True, 'warnings': True, 'prefix': '#&', 'escape': None,
                   'zfile': False, 'zold': False}

id_ignore_override = 0  # used to avoid overriding a file without the possibility to create a .zold file

options = default_options

unknown_options = []
zswap_options_help = []
zswap_options_description = dict()


# :help=?
zswap_options_description['override'] = '''
    Overwrite the file with the result
'''
zswap_options_description['overwrite'] = zswap_options_description['override']
zswap_options_description['no-output'] = '''
    Doesn't show the result
'''
zswap_options_description['no-errors'] = '''
    Doesn't show any errors
'''
zswap_options_description['no-warnings'] = '''
    Doesn't show any warnings
'''
zswap_options_description['zold'] = '''
    Write the result to a file with the ".zold" extension
    (Automatically enable ":override" if the ".zold" file could be created)
'''
zswap_options_description['zfile'] = '''
    Write the result to a file with the ".zfile" extension
'''
zswap_options_description['prefix'] = '''
    Set a custom prefix
'''
zswap_options_description['escape'] = '''
    Escape a string in included files
'''


zswap_help = '''
<[ zswap\'s help ]>

    Usage :
        zswap :options files

    Options :
        :override
        :overwrite -> :override
        :no-output
        :no-errors
        :no-warnings
        :zfile
        :zold
        :prefix=?
        :escape=?
        :help=? (eg: "zswap :help=override")

    zswap tag :
        #&zswap<path/to/file>

    About :
        Created by frk2z (@FrK2z)
        Version : 1.0.0

<[ end help ]>
'''


def replace(in_string, replace_string, replace_by):
    return replace_by.join(in_string.split(replace_string))


# Any arguments that start with ':' is considered as an option
def is_option(in_string):
    if in_string[0] == ':':
        return True
    return False


# Get argument from option
def option_arg_search(argument, option_search):
    r = re.compile(':' + option_search + '=(.*)')
    m = r.findall(argument)
    if m:
        return m[0]


# Used to search zswap tag in a string
def zswap_search(prefix_string, in_string):
    r = re.compile(prefix_string + 'zswap<(.*?)>')
    m = r.findall(in_string)
    if m:
        return m
    else:
        return ''


# If the user didn't put any arguments
if len(sys.argv) < 2:

    print(zswap_help)

else:

    count = 0

    for i in sys.argv:
        if is_option(i):
            if i == ':override' or i == ':overwrite':
                options['override'] = True
            elif i == ':no-output':
                options['output'] = False
            elif i == ':no-errors':
                options['errors'] = False
            elif i == ':no-warnings':
                options['warnings'] = False
            elif i == ':zfile':
                options['zfile'] = True
            elif i == ':zold':
                options['override'] = True
                options['zold'] = True
            else:
                prefix_option = option_arg_search(i, 'prefix')
                escape_option = option_arg_search(i, 'escape')
                help_option = option_arg_search(i, 'help')
                if prefix_option:  # :prefix=?
                    options['prefix'] = prefix_option
                elif escape_option:  # :escape=?
                    options['escape'] = escape_option
                elif help_option:  # :help=?
                    zswap_options_help.append(help_option)
                else:
                    unknown_options.append(i)

    if options['errors']:
        # Show an error for each unknown option
        for u in unknown_options:
            print('ERROR: Unknown option "' + u + '"')

    if len(zswap_options_help) > 0:
        for option in zswap_options_help:
            try:
                option_help = zswap_options_description[option]
                print('\n<[ ' + option + "'s help ]>")
                print(option_help)
                print('<[ end help ]>\n')
            except KeyError:
                if option == 'zswap':
                    # :help=zswap
                    print(zswap_help)
                else:
                    print('ERROR: Unknown option "' + option + '"')

    for i in sys.argv:

        if count > 0 and not is_option(i):

            try:
                open_file = open(i, 'r')
                open_file_content = open_file.read()
                open_file.close()

                if options['zold']:
                    # Make a backup file
                    try:
                        zold_file = open(i + '.zold', 'w')
                        zold_file.write(open_file_content)
                        zold_file.close()
                    except IOError:
                        # In case the zold file couldn't be writen, the override option is disabled
                        id_ignore_override = count
                        if options['errors']:
                            print('ERROR: Unable to write file "' + i + '.zold"')

                result = zswap_search(options['prefix'], open_file_content)
                file_result = open_file_content

                if not result == '':
                    for path in result:

                        try:
                            tagged_file = open(path, 'r')
                            tagged_file_content = tagged_file.read()
                            tagged_file.close()

                            if options['escape']:
                                tagged_file_content = replace(tagged_file_content, options['escape'],
                                                              '\\' + options['escape'])

                            file_result = replace(file_result, options['prefix'] + 'zswap<' + path + '>',
                                                  tagged_file_content)
                        except IOError:
                            if options['errors']:
                                print('ERROR: Unable to read file "' + path +
                                      '" included by a zswap tag in "' + i + '"')

                    if options['output']:
                        print(file_result)
                    if options['override'] and id_ignore_override != count:
                        try:
                            write_file = open(i, 'w')
                            write_file.write(file_result)
                            write_file.close()

                        except IOError:
                            if options['errors']:
                                print('ERROR: Unable to write file "' + i + '"')
                    if options['zfile']:
                        try:
                            write_zfile = open(i + '.zfile', 'w')
                            write_zfile.write(file_result)
                            write_zfile.close()

                        except IOError:
                            if options['errors']:
                                print('ERROR: Unable to write file "' + i + '.zfile"')

                else:
                    if options['warnings']:
                        print('WARNING: "' + i + "\" doesn't have any zswap tag")

                    if options['output']:
                        print(open_file_content)

            except IOError:
                if options['errors']:
                    print('ERROR: Unable to read file "' + i + '"')

        count += 1

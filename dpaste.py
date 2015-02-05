import sublime
import sublime_plugin

try:
    from urllib.parse import urlencode
    from urllib.request import urlopen
except ImportError:
    from urllib import urlopen, urlencode

API_URL = 'http://dpaste.com/api/v2/'
SYNTAX_DICT = {
    'coffee': 'coffee-script',
    'text': 'text',
    'tcl': 'tcl',
    'cs': 'csharp',
    'go': 'go',
    'xml': 'xml',
    'erl': 'erlang',
    'py': 'python3',
    'dart': 'dart',
    'nginx': 'nginx',
    'bat': 'bat',
    'scala': 'scala',
    'applescript': 'applescript',
    'lua': 'lua',
    'rb': 'rb',
    'js': 'js',
    'c': 'c',
    'vb': 'vb.net',
    'clj': 'clojure',
    'hs': 'haskell',
    'diff': 'diff',
    'java': 'java',
    'yaml': 'yaml',
    'pl': 'perl',
    'json': 'json',
    'rst': 'rst',
    'scm': 'scheme',
    'erb': 'erb',
    'm': 'objective-c',
    'cobol': 'cobol',
    'ini': 'ini',
    'io': 'io',
    'haml': 'haml',
    'mako': 'mako',
    'html': 'html',
    'css': 'css',
    'jsp': 'jsp',
    'sql': 'sql',
    'php': 'php',
    'scss': 'scss',
    'sass': 'sass',
    'jinja': 'django',
    'cpp': 'cpp',

    # some of my mapping
    'htm': 'html',
    'jinja2': 'django',
    'less': 'css',  # no support for less yet
}


class DpasteCommand(sublime_plugin.TextCommand):
    def _get_syntax_from_file_extension(self):
        ext = ''
        try:
            _, _, ext = self.view.file_name().rpartition('.')
        except AttributeError:
            pass
        except TypeError:
            pass
        return SYNTAX_DICT.get(ext, 'text')

    def run(self, edit):
        # get the content from selection
        content = '\r\n'.join([
            self.view.substr(region)
            for region in self.view.sel()
            if not region.empty()
        ])

        # if nothing is selected, get the whole file content
        if not content:
            content = self.view.substr(sublime.Region(0, self.view.size()))

        if content:
            dpaste_url = ''
            try:
                # send request with content and syntax
                response = urlopen(url=API_URL, data=urlencode({
                    'content': content,
                    'syntax': self._get_syntax_from_file_extension()
                }).encode('utf8'))
                dpaste_url = response.headers['Location']
            except:
                sublime.status_message('Dpaste Sublime error: Request error')

            # copy to clipboard if everything is fine
            if dpaste_url != '':
                sublime.set_clipboard(dpaste_url)
                sublime.status_message(
                    'Dpaste URL copied to clipboard: ' + dpaste_url
                )
        else:
            sublime.status_message('Dpaste Sublime error: Nothing selected')

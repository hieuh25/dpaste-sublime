import sublime
import sublime_plugin

try:
    from urllib.parse import urlencode
    from urllib.request import urlopen
except ImportError:
    from urllib import urlopen, urlencode

API_URL = 'http://dpaste.com/api/v2/'
SYNTAX_DICT = {
    'py': 'python2',
    'php': 'php',
    'txt': 'text',
    'htm': 'html',
    'html': 'html',
    'jinja': 'django',
    'js': 'js',
    'coffee': 'coffee-script',
    'css': 'css',
    'sass': 'sass',
    'scss': 'scss',
    'less': 'css',  # no support for less yet
    'sql': 'sql'
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
        content = u''

        # get the content from selection
        for region in self.view.sel():
            if not region.empty():
                # insert new line if there are multiple selections
                if content:
                    content += '\r\n'
                content += self.view.substr(region)

        if content:
            dpaste_url = ''
            try:
                # send request with content and syntax
                response = urlopen(url=API_URL, data=urlencode({
                    'content': content,
                    'syntax': self._get_syntax_from_file_extension()
                }).encode('utf8'))
                dpaste_url = response.geturl()
            except:
                sublime.status_message('dpaste-sublime error: Request error')

            if dpaste_url != '':
                sublime.set_clipboard(dpaste_url)
                sublime.status_message(
                    'dpaste URL copied to clipboard: ' + dpaste_url
                )
        else:
            sublime.status_message('dpaste-sublime error: Nothing selected')

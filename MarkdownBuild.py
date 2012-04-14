import sublime
import sublime_plugin
import markdown_python
import os
import tempfile
import subprocess
import webbrowser


class MarkdownBuild(sublime_plugin.WindowCommand):
    def run(self):
        view = self.window.active_view()
        if not view:
            return
        file_name = view.file_name()
        if not file_name:
            return
        contents = view.substr(sublime.Region(0, view.size()))
        md = markdown_python.markdown(contents)
        html = '<html><meta charset="UTF-8">'
        css = os.path.join(sublime.packages_path(), 'MarkdownBuild', 'markdown.css')
        if (os.path.isfile(css)):
            styles = open(css, 'r').read()
            html += '<style>' + styles + '</style>'
        html += "<body>"
        html += md
        html += "</body></html>"
        s = sublime.load_settings("Preferences.sublime-settings")
        output_in_same_dir = s.get("markdownbuild_output_same_dir", 0)
        if output_in_same_dir:
            path = os.path.dirname(file_name)
            file_name = os.path.basename(file_name)
            base_name = os.path.splitext(file_name)[0]
            html_file = path + "/" + base_name + ".html"
            f = open(html_file, 'w')
            f.write(html.encode('UTF-8'))
            f.close()
            webbrowser.open("file://" + html_file)
        else:
            output = tempfile.NamedTemporaryFile(delete=False, suffix='.html')
            output.write(html.encode('UTF-8'))
            output.close()
            webbrowser.open("file://" + output.name)

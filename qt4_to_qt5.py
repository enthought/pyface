import re
import os, os.path

import importlib


class FileUpdater(object):

    submodules = ['QtCore', 'QtGui', 'QtWidgets', 'QtPrintSupport', 'QtSvg', 'QtWebKit', 'QtWebKitWidgets']


    def __init__(self):
        
        self.parent_dict = dict()
        for name in self.submodules:
            module = importlib.import_module('PyQt5.' + name)
            members = [m for m in module.__dict__.keys() if m[0] is not '_'] # list of public module members
            self.parent_dict.update( (m, name) for m in members) #mapping of members to parent module name
        self.parent_dict.update({'Signal': 'QtCore'})

        # search for 'submodule.member', e.g. QtWidgets.QWidget
        self.pattern = '(?P<old_parent>' + '|'.join(self.submodules) + ')' + '\.(?P<child>[a-zA-Z0-9_]+)'
        
    
    def update(self, filename):
        self.imports_used = set()
        self.failures = []
        self.n_changes = 0
        code = open(filename).read()
        modified_code = re.sub(self.pattern, self.rename_modules, code)

        modified_code = re.sub('from pyface.qt import (?P<imports>.*$)',
                               self.update_import,
                               modified_code,
                               flags=re.MULTILINE,
                               count=1)
        
        return self.n_changes, self.imports_used, self.failures, modified_code

    def rename_modules(self, match):
        child = match.group('child')
        parent = self.parent_dict.get(child)
        old_snippet = match.group(0)
        if parent is None:
            #print "Error, parent not found for snippet", old
            new_snippet = old_snippet #no changes in code
            self.failures.append(old_snippet)
            self.imports_used.add(match.group('old_parent'))
        else:
            self.imports_used.add(parent)
            new_snippet = parent + '.' + child

        if old_snippet != new_snippet:
            self.n_changes += 1
            #print old, ' -> ', new

        return new_snippet

    def update_import(self, match):
        """update 'from pyface.qt import xxx' to used imports (self.imports_used)"""
        #print 'found imports:'
        #print match.group(0)
        imports = match.groups('imports')[0].split(',')
        imports = [s.strip() for s in imports]
        qt_imports = [s for s in imports if s.startswith('Qt')]
        other_imports = [s for s in imports if not s.startswith('Qt')]

        #make consistent order: like in self.submodules + other_imports at end
        modified_imports = [s for s in self.submodules if s in self.imports_used] + sorted(other_imports)
            
        new_snippet = "from pyface.qt import %s"%(', '.join(modified_imports))

        if match.group(0) != new_snippet:
            self.n_changes += 1
            
        #print new_snippet
        return new_snippet
    
        

updater = FileUpdater()

def walk(root='pyface/ui/qt5', replace_files = False):

    for root, dirs, files in os.walk(root):
        py_files = [f for f in files if f.endswith('.py')]

        for file in py_files:
            full_path = os.path.join(root, file)
            n_changes, imports, failures, modified = updater.update(full_path)

            if n_changes>0 or failures: # or imports:
                print full_path
                print '%d changes'%n_changes
            else:
                continue

            if imports:
                print 'imports used:', ', '.join(imports)

            if failures:
                print 'failures:'
                for x in failures:
                    print x

            if replace_files:
                out = open(full_path, 'w')
                out.write(modified)
                out.close()

            print 

def update_file(filename, replace_file=False):
    n_changes, imports, failures, modified = updater.update(filename)
    print filename
    print "%d changes"%n_changes
    if imports:
        print 'from pyface.qt import %s'%', '.join(imports)

    if failures:
        print 'failures:'
        for x in failures:
            print x
    print
    #print modified
    if replace_file:
        out = open(filename, 'w')
        out.write(modified)
        out.close()




#update_file('pyface/ui/qt5/about_dialog.py', replace_file = False)
#update_file('pyface/ui/qt5/application_window.py', replace_file = False)

walk(replace_files=False)



#update_file('../traitsui/traitsui/qt5/boolean_editor.py', replace_file = True)
#walk('../traitsui/traitsui/qt5', replace_files = False)

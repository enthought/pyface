from pyface.toolkit import toolkit

if toolkit.toolkit == "wx":
    from python_editor_wx import PythonEditor
elif toolkit.toolkit == "qt":
    from python_editor_qt import PythonEditor
else:
    raise RuntimeError("Unsupported toolkit %s" % toolkit.toolkit)

COL_WIDTH = 20


def text_to_columns(text):
    """Split text (input arg) to columns, the amount of double
       newlines (\n\n) in text determines the amount of columns.
       Return a string with the column output like:
       line1\nline2\nline3\n ... etc ...
       See also the tests for more info."""
    parts = text.split('\n\n')
    result = ''
    while any(len(part) > 0 for part in parts):
        idx = [(part+' ').rfind(' ', 0, COL_WIDTH+1) for part in parts]
        result += ' '.join([f'{part[:ind].strip():{COL_WIDTH}}'
                            for ind, part in zip(idx, parts)]) + '\n'
        parts = [part[ind+1:] for ind, part in zip(idx, parts)]
    return result

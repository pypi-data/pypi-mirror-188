from puissant import *
import pytest
from io import StringIO

def test_yes_no(monkeypatch, capsys):
    monkeypatch.setattr('builtins.input', lambda _:'y')
    o = yes_no('is this ok')
    assert o == True
    captured = capsys.readouterr()
    assert captured.out == 'is this ok [y/n]?'
    
    monkeypatch.setattr('builtins.input', lambda _:'yes')
    o = yes_no('is this ok')
    assert o == True
    captured = capsys.readouterr()
    assert captured.out == 'is this ok [y/n]?'

    monkeypatch.setattr('builtins.input', lambda _:'Y')
    o = yes_no('is this ok')
    assert o == True
    captured = capsys.readouterr()
    assert captured.out == 'is this ok [y/n]?'
    
    monkeypatch.setattr('builtins.input', lambda _:'YES')
    o = yes_no('is this ok')
    assert o == True
    captured = capsys.readouterr()
    assert captured.out == 'is this ok [y/n]?'

    monkeypatch.setattr('builtins.input', lambda _:'n')
    o = yes_no('is this ok')
    assert o == False
    captured = capsys.readouterr()
    assert captured.out == 'is this ok [y/n]?'
    
    monkeypatch.setattr('builtins.input', lambda _:'no')
    o = yes_no('is this ok')
    assert o == False
    captured = capsys.readouterr()
    assert captured.out == 'is this ok [y/n]?'

    monkeypatch.setattr('builtins.input', lambda _:'N')
    o = yes_no('is this ok')
    assert o == False
    captured = capsys.readouterr()
    assert captured.out == 'is this ok [y/n]?'
    
    monkeypatch.setattr('builtins.input', lambda _:'NO')
    o = yes_no('is this ok')
    assert o == False
    captured = capsys.readouterr()
    assert captured.out == 'is this ok [y/n]?'

    monkeypatch.setattr('builtins.input', lambda _:'invalid value')
    with pytest.raises(ValueError):
        yes_no('is this ok', retries = 1)
        
    captured = capsys.readouterr()
    assert captured.out == 'is this ok [y/n]? input must be one of y, n, yes, no.\nis this ok [y/n]? input must be one of y, n, yes, no.\n'

def test_tickbox_menu(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', StringIO('a\nd\n'))
    assert tickbox_menu('animal:',['lion','cat','dog','zebra']) == [(0, 'lion'), (1, 'cat'), (2, 'dog'), (3, 'zebra')]

    monkeypatch.setattr('sys.stdin', StringIO('a\nn\nd\n'))
    assert tickbox_menu('animal:',['lion','cat','dog','zebra']) == []

    monkeypatch.setattr('sys.stdin', StringIO('1\nn\nd\n'))
    assert tickbox_menu('animal:',['lion','cat','dog','zebra']) == []

    monkeypatch.setattr('sys.stdin', StringIO('1\nd\n'))
    assert tickbox_menu('animal:',['lion','cat','dog','zebra']) == [(0, 'lion')]
    
def test_tickbox_menu_out(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', StringIO('d\n'))
    assert tickbox_menu('animal:',['lion','cat','dog','zebra']) == []
    captured = capsys.readouterr()
    assert captured.out == 'animal:\n1  [ ] - lion\n2  [ ] - cat\n3  [ ] - dog\n4  [ ] - zebra\n\n- type a number to tick the option.\n- "a" selects all.\n- "n" de-selects all.\n- "d" selection done.\n\nOption? : '
    
def test_menu(monkeypatch, capsys):
    monkeypatch.setattr('builtins.input', lambda _: 1)
    m = menu('pick up a fruit:', ['orange', 'apple', 'banana'])
    assert m == 'orange'
    captured = capsys.readouterr()
    assert captured.out == 'pick up a fruit:\n 1 - orange\n 2 - apple\n 3 - banana\nselect an item [range: 1..3]: '

    monkeypatch.setattr('builtins.input', lambda _: 2)
    m = menu('pick up a fruit:', ['orange', 'apple', 'banana'])
    assert m == 'apple'
    captured = capsys.readouterr()
    assert captured.out == 'pick up a fruit:\n 1 - orange\n 2 - apple\n 3 - banana\nselect an item [range: 1..3]: '

    monkeypatch.setattr('builtins.input', lambda _: 3)
    m = menu('pick up a fruit:', ['orange', 'apple', 'banana'])
    assert m == 'banana'
    captured = capsys.readouterr()
    assert captured.out == 'pick up a fruit:\n 1 - orange\n 2 - apple\n 3 - banana\nselect an item [range: 1..3]: '
    
    monkeypatch.setattr('builtins.input', lambda _:'orange')
    with pytest.raises(ValueError):
        m = menu('pick up a fruit:', ['orange', 'apple', 'banana'], retries = 0)
    captured = capsys.readouterr()
    assert captured.out == 'pick up a fruit:\n 1 - orange\n 2 - apple\n 3 - banana\nselect an item [range: 1..3]: input must be of type int.\n'

    monkeypatch.setattr('builtins.input', lambda _:'4')
    with pytest.raises(ValueError):
        m = menu('pick up a fruit:', ['orange', 'apple', 'banana'], retries = 0)
    captured = capsys.readouterr()
    assert captured.out == 'pick up a fruit:\n 1 - orange\n 2 - apple\n 3 - banana\nselect an item [range: 1..3]: input must be in range 1..3.\n'

def test_enum_str(monkeypatch, capsys):
    monkeypatch.setattr('builtins.input', lambda _: 'a')
    l = enum_str('pick a letter',['a','b','c'])
    assert l == 'a'
    captured = capsys.readouterr()
    assert captured.out == 'pick a letter (valid choices: a, b, c):\n'

    monkeypatch.setattr('builtins.input', lambda _: 'b')
    l = enum_str('pick a letter',['a','b','c'], quiet = True)
    assert l == 'b'
    captured = capsys.readouterr()
    assert captured.out == 'pick a letter: '
    
    monkeypatch.setattr('builtins.input', lambda _: 'd')
    with pytest.raises(ValueError):
        enum_str('pick a letter',['a','b','c'], quiet = True, retries = 0)
    captured = capsys.readouterr()
    assert captured.out == 'pick a letter:  input must be one of a, b, c.\n'


def test_ranged_int(monkeypatch, capsys):
    monkeypatch.setattr('builtins.input', lambda _: '0')
    i = ranged_int('enter number', 0,10)
    assert i == 0
    captured = capsys.readouterr()
    assert captured.out == 'enter number [range: 0..10]: '

    monkeypatch.setattr('builtins.input', lambda _: '12')
    with pytest.raises(ValueError):
        i = ranged_int('enter number', 0,10, retries = 0)
    captured = capsys.readouterr()
    assert captured.out == 'enter number [range: 0..10]: input must be in range 0..10.\n'

    monkeypatch.setattr('builtins.input', lambda _: '10')
    i = ranged_int('enter number', 0,10, default = 5)
    assert i == 10
    captured = capsys.readouterr()
    assert captured.out == 'enter number [range: 0..10]: (default:5) '

    monkeypatch.setattr('builtins.input', lambda _: '')
    i = ranged_int('enter number', 0,10, default = 5)
    assert i == 5
    captured = capsys.readouterr()
    assert captured.out == 'enter number [range: 0..10]: (default:5) '
    

def test_ranged_float(monkeypatch, capsys):
    monkeypatch.setattr('builtins.input', lambda _: '1.0')
    i = ranged_float('enter number', 0.0,10.0)
    assert i == 1.0
    captured = capsys.readouterr()
    assert captured.out == 'enter number [range: 0.0..10.0]: '

    monkeypatch.setattr('builtins.input', lambda _: '12.0')
    with pytest.raises(ValueError):
        i = ranged_float('enter number', 0.0,10.0, retries = 0)
    captured = capsys.readouterr()
    assert captured.out == 'enter number [range: 0.0..10.0]: input must be in range 0.0..10.0.\n'

    monkeypatch.setattr('builtins.input', lambda _: '9.1')
    i = ranged_float('enter number', 0.0,10.0, default = 5.0)
    assert i == 9.1
    captured = capsys.readouterr()
    assert captured.out == 'enter number [range: 0.0..10.0]: (default:5.0) '

    monkeypatch.setattr('builtins.input', lambda _: '')
    i = ranged_float('enter number', 0.0,10.0, default = 5.0)
    assert i == 5.0
    captured = capsys.readouterr()
    assert captured.out == 'enter number [range: 0.0..10.0]: (default:5.0) '

def test_vinput(monkeypatch, capsys):
    with pytest.raises(ValueError):
        i = vinput('myprompt',typ = float, nrange = (0.1, 10.0), enum = [1.0,2.0,3.0])

    monkeypatch.setattr('sys.stdin', StringIO('a\n0.3\n'))
    assert vinput('myprompt',typ = float, nrange = (0.1, 10.0), type_err_msg= "ERROR") == 0.3

    monkeypatch.setattr('sys.stdin', StringIO('11.0\n0.5\n'))
    assert vinput('myprompt',typ = float, nrange = (0.1, 10.0), range_err_msg= "ERROR") == 0.5

    monkeypatch.setattr('sys.stdin', StringIO('11.0\n0.1\n'))
    assert vinput('myprompt',typ = float, enum = (0.1, 10.0), enum_err_msg= "ERROR") == 0.1

    def valfn(_): return False
    with pytest.raises(ValueError):
        monkeypatch.setattr('sys.stdin', StringIO('0.1\n10.0\n'))
        vinput('myprompt',typ = float, nrange = (0.1, 10.0), range_err_msg= "ERROR", validation_fn = valfn, retries = 1)
        
        
    
    
                        
    

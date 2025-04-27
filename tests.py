import main
import pytest

@pytest.fixture()
def get_true_report_dict() -> dict:
    d = {
        '/admin/dashboard/' : { 'DEBUG'    : 1,
                                'ERROR'   : 6,
                                'CRITICAL': 2
                                },
        '/api/v1/payments'  : { 'DEBUG'    : 5,
                                'INFO'    : 4, 
                                'WARNING' : 3,
                                'ERROR'   : 32
                                },
        ' '                 : { 'DEBUG'    : 6,
                                'INFO'    : 4, 
                                'WARNING' : 3,
                                'ERROR'   : 38,
                                'CRITICAL': 2
                                }        
    }
    return d

@pytest.fixture()
def get_empty_report_dict() -> dict:
    return {}

@pytest.fixture()
def get_true_log_file() -> list:
    logs = ['logs\\app1.log', 'logs\\app2.log', 'logs\\app3.log']
    return logs

@pytest.fixture()
def get_fail_log_file() -> list:
    logs = ['logs\\app11.log']
    return logs

def test_show_report(get_true_report_dict, get_true_log_file) -> None:
    t = main.TzLogger()
    t.args.log = get_true_log_file                        
    t.args.report = 'handlers'
    t.data = get_true_report_dict
    got = t.show_report()
    assert got == True

def test_show_report_with_non_exists_log(get_fail_log_file) -> None:
    t = main.TzLogger()
    t.args.log = get_fail_log_file
    t.args.report = 'handlers'
    t.data = t.read_log()
    got = t.show_report()
    assert got == True


def test_show_report_with_name_error() -> None:
    t = main.TzLogger()
    t.args.report = 'fail'
    got = t.show_report()
    assert got == False

def test_show_report_with_empty_data(get_empty_report_dict) -> None:
    t = main.TzLogger()
    t.args.report = 'handlers'
    t.data = get_empty_report_dict
    got = t.show_report()
    assert got == True

def test_read_log_with_true_files(get_true_log_file) -> None:
    t = main.TzLogger()
    t.args.log = get_true_log_file
    t.args.report = 'handlers'
    d = t.read_log()
    assert type(d) == dict    

def test_read_log_with_empty_file() -> None:
    t = main.TzLogger()
    t.args.log = ['logs\\empty.log']
    t.args.report = 'handlers'
    d = t.read_log()
    assert d == {}
    
def test_read_log_withot_log_files() -> None:
    t = main.TzLogger()
    t.args.log = []
    t.args.report = 'handlers'
    d = t.read_log()
    assert d == {}
    
def test_read_log_withot_needed_handlers() -> None:
    t = main.TzLogger()
    t.args.log = ['logs\\withot_handlers.log']
    t.args.report = 'handlers'
    d = t.read_log()
    assert d == {}

def test_read_log_with_crashed_data() -> None:
    t = main.TzLogger()
    t.args.log = ['logs\\crash.log']
    t.args.report = 'handlers'
    d = t.read_log()
    assert type(d) == dict and ' ' in d


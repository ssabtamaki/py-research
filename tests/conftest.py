import json
from pytest import fixture


@fixture(scope='function')
def create_jsonfile(tmpdir):
    data = {"full_text": "野球が好き"}
    tmpfile = tmpdir.join('text.json')
    with tmpfile.open('w') as f:
        json.dump(
            data, f, ensure_ascii=False, indent=4,
            sort_keys=True, separators=(',', ': ')
        )
    yield str(tmpfile)
    tmpfile.remove()


@fixture(scope='function')
def create_jsonfiles(tmpdir):
    # 前処理のcreate_jsonfileを10回行ってリストを返したい
    data = [({"full_text": "野球が好き"}, "test1.json"),
            ({"full_text": "野球は楽しくないし、嫌い"}, "test2.json"),
            ({"full_text": "野球をプレイする"}, "test3.json")
            ]
    jsonfiles = list()
    for d in data:
        tmpfile = tmpdir.join(d[1])
        with tmpfile.open('w') as f:
            json.dump(
                d[0], f, ensure_ascii=False, indent=4,
                sort_keys=True, separators=(',', ': ')
            )
        jsonfiles.append(tmpfile)
    yield jsonfiles
    for f in jsonfiles:
        f.remove()


def test_fixture(create_jsonfiles, tmpdir):
    expected = [f"{tmpdir}/test1.json",
                f"{tmpdir}/test2.json", f"{tmpdir}/test3.json"]
    jsonfiles = create_jsonfiles
    print(jsonfiles)
    for i in jsonfiles:
        if i not in expected:
            assert False, "{0}".format(i)
    assert True

import remotivelabs.broker.sync as br

def test_sha256_random():
    assert br.get_sha256('tests/random.bin') == '88f2c5751614b5140b8865890dd61df671d792ad94502d4eaff45d14b55e5539'

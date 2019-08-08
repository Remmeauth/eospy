import sys
sys.path.append('../eospy')

import eospy.cleos
import requests
from nose.tools import raises

class TestCleos :

    def setup(self) :
        self.ce = eospy.cleos.Cleos('https://api.pennstation.eosnewyork.io:7101')
        self.json_to_bin = {u'to': u'rem', u'memo': u'test', u'from': u'rem', u'quantity': u'1.0000 EOS'}
        self.bin_to_json = '0000000000ea30550000000000ea3055102700000000000004454f53000000000474657374'

    def test_get_info(self) :
        output = self.ce.get_info()
        # test output is valid
        assert "server_version" in output
        assert "chain_id" in output
        assert "head_block_num" in output
        assert "last_irreversible_block_num" in output
        assert "head_block_id" in output
        assert "head_block_producer" in output
        assert "virtual_block_cpu_limit" in output
        assert "virtual_block_net_limit" in output
        assert "block_cpu_limit" in output
        assert "block_net_limit" in output

    def test_get_block(self) :
        block = self.ce.get_block(1)
        assert block['block_num'] == 1

    @raises(requests.exceptions.HTTPError)
    def test_get_block_invalid(self) :
        block = self.ce.get_block(-1)
        
    def test_get_account(self) :
        acct = self.ce.get_account('rem')
        assert acct['account_name'] == 'rem'

    @raises(requests.exceptions.HTTPError)
    def test_get_account_invalid(self) :
        acct = self.ce.get_account('remremrem')

    def test_get_abi(self) :
        abi = self.ce.get_abi('rem')

    def test_get_code(self) :
        code = self.ce.get_code('rem')

    def test_get_code_bad(self) :
        code = self.ce.get_code('rem.ram')
        assert code['code_hash'] == u'0000000000000000000000000000000000000000000000000000000000000000'

    def test_get_table(self):
        table = self.ce.get_table('rem','rem', 'producers', lower_bound='eosnewyorkio')

    @raises(requests.exceptions.HTTPError)
    def test_get_table_bad(self):
        table = self.ce.get_table('rem', 'rem', 'producer')

    def test_get_currency_balance(self) :
        bal = self.ce.get_currency_balance('rem', 'rem.token', 'EOS')

    @raises(requests.exceptions.HTTPError)
    def test_get_currency_balance_fail(self) :
        bal = self.ce.get_currency_balance('rem', 'rem', 'SYS')

    def test_json_to_bin(self) :
        bin = self.ce.abi_json_to_bin('rem.token', 'transfer', self.json_to_bin)
        assert bin['binargs'] == self.bin_to_json

    @raises(requests.exceptions.HTTPError)
    def test_json_to_bin_bad(self) :
        bin = self.ce.abi_json_to_bin('rem.token', 'transfer', '')
        assert bin['binargs'] == ''

    def test_bin_to_json(self) :
        bin = self.ce.abi_bin_to_json('rem.token', 'transfer', self.bin_to_json)
        assert bin['args'] == self.json_to_bin

    @raises(requests.exceptions.HTTPError)
    def test_bin_to_json_fail(self) :
        bin = self.ce.abi_bin_to_json('rem.token', 'transfer', '00')

    def test_get_currency_stats(self) :
        self.ce.get_currency_stats('rem.token', 'EOS')

    def test_get_currency_stats_bad(self) :
        stats = self.ce.get_currency_stats('rem.token', 'SYS')
        assert stats == {}

    def test_get_producers(self) :
        self.ce.get_producers()

    

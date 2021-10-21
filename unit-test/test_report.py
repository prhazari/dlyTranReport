import unittest
import logging
import os
from util.report import parse_args, write_csv, genDlyTransRep

class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.inputfile = 'Input.txt'
        self.outfile = 'Output.csv'
        logging.basicConfig(format=' [%(asctime)s][%(levelname)s] %(message)s',
                            level=logging.INFO)

    def tearDown(self):
        if os.path.exists(self.outfile):
            os.remove(self.outfile)


    """
    def test_parse_args(self):
        self.assertIsNotNone(parse_args())  # add assertion here
    """
    
    def test_write_csv(self):
        with self.assertRaises(ValueError) as exception_context:
            write_csv('hello', None, 'test')
        self.assertEqual(
            str(exception_context.exception),
            "One of the inputs argument is Null"
        )

    def test_genDlyTransRep_arg_check(self):
        with self.assertRaises(ValueError) as exception_context:
            genDlyTransRep('hello', None, logging)
        self.assertEqual(
            str(exception_context.exception),
            "One of the inputs argument is Null"
        )

    def test_genDlyTransRep_inputfile_notexists(self):
        with self.assertRaises(ValueError) as exception_context:
            genDlyTransRep('hello', logging)
        self.assertEqual(
            str(exception_context.exception),
            "Input file hello does not exists"
        )

    def test_genDlyTransRep_inputfile_emty(self):
        with self.assertRaises(ValueError) as exception_context:
            genDlyTransRep('Empty.txt', logging)
        self.assertEqual(
            str(exception_context.exception),
            "Input file Empty.txt is empty"
        )

    def test_genDlyTransRep_outfile_wrong_outfile_ext(self):
        with self.assertRaises(ValueError) as exception_context:
            genDlyTransRep('Input.txt', logging, 'Output.txt')
        self.assertEqual(
            str(exception_context.exception),
            "Wrong output file extension: [.txt]!! Expected .csv"
        )

    def test_genDlyTransRep_outfile_path_donexists(self):
        with self.assertRaises(ValueError) as exception_context:
            genDlyTransRep('Input.txt', logging, '/dontexists/Output.csv')
        self.assertEqual(
            str(exception_context.exception),
            "Output file directory[/dontexists] does not exists!!"
        )

    def test_genDlyTransRep_success(self):
        self.assertEqual(True,
                         genDlyTransRep(self.inputfile, logging, self.outfile))

if __name__ == '__main__':
    unittest.main()

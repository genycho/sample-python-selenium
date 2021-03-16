import unittest
import xmlrunner


def runner(output='test_result'):
    return xmlrunner.XMLTestRunner(
        output=output
    )


def find_tests():
    return unittest.TestLoader().discover('tests')


if __name__ == '__main__':
    runner().run(find_tests())


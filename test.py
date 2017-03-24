import unittest
from TextFile import num_to_pitch_class_with_oct
class SimpleTest(unittest.TestCase):
    def test_num_to_pitch_class_with_oct(self):
        final = ['c', 'd', 'e', 'f', 'g', 'a', 'b']
        oct = [4] * 14
        num = '%*-0123456789>'
        for i, element in enumerate(final):
            oct = [4] * 14
            oct2 = [4] * 14
            (pitch_class, oct) = num_to_pitch_class_with_oct(num, element, oct)
            ptr = num.find('1') # get the tonic position
            for j, element2 in enumerate(num):
                des = i + j - ptr
                while(des < 0):
                    des += len(final)
                    oct2[j] -= 1
                while(des >= len(final)):
                    des -= len(final)
                    oct2[j] += 1
                self.assertEqual(pitch_class[j], final[des])
                self.assertEqual(oct[j], oct2[j])
            print(pitch_class, oct)

if __name__ == '__main__':
    unittest.main()

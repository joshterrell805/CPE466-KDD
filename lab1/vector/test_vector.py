import unittest
import math
from vector import Vector

class TestVectorHandling(unittest.TestCase):

  def test_length(self):
    vec = Vector([3,4])
    length = vec.length()
    self.assertEqual(length, 5)

  def test_dot_product(self):
    vec = Vector([1,2])
    by = Vector([3,4])
    dot = vec.dot(by)
    self.assertEqual(11, dot)

  def test_euclidian(self):
    vec = Vector([-1,2])
    pair = Vector([3,5])
    dist = vec.euclidDist(pair)
    self.assertEqual(5, dist)

  def test_manhattan(self):
    vec = Vector([1,2])
    pair = Vector([3,4])
    dist = vec.manhattanDist(pair)
    self.assertEqual(4, dist)

  def test_mean(self):
    vec = Vector([1,2,3])
    mean = vec.mean()
    self.assertEqual(2, mean)

  def test_covariance(self):
    vec = Vector([1,2,3])
    pair = Vector([4,6,8])
    cov = vec.covariance(pair)
    self.assertEqual(4/3, cov)

  def test_std_dev(self):
    vec = Vector([1,2,3])
    stdDev = vec.stdDev()
    self.assertEqual(math.sqrt(2/3), stdDev)

  def test_pearson_correlation(self):
    vec = Vector([1,2,3])
    pair = Vector([4,6,8])
    dist = vec.pearsonCorrelation(pair)
    self.assertEqual((4/3)/(math.sqrt(2/3) * math.sqrt(8/3)), dist)

  def test_largest(self):
    vec = Vector([1,2,3])
    lrg = vec.largest()
    self.assertEqual(3, lrg)

  def test_smallest(self):
    vec = Vector([1,2,3])
    smallest = vec.smallest()
    self.assertEqual(1, smallest)

  def test_median(self):
    vec = Vector([1,2,3])
    median = vec.median()
    self.assertEqual(2, median)

  def columnData(self):
    data = [[1,2,3],
        [4,5,6],
        [3,2,1]]
    return map(Vector, data)

  def test_rotateMatrix(self):
    vector = self.columnData()
    vec = Vector.rotate(vector)
    self.assertEqual([Vector([1,4,3]),
                      Vector([2,5,2]),
                      Vector([3,6,1])], vec)

  def test_column_largest(self):
    vector = self.columnData()
    lrg = [vec.largest() for vec in Vector.rotate(vector)]
    self.assertEqual([4,5,6], lrg)

  @unittest.skip("unimplemented")
  def test_column_smallest(self):
    vectors = self.columnData()
    smallest = Vector.smallest(vectors)
    self.assertEqual([1,2,1], smallest)

  @unittest.skip("unimplemented")
  def test_column_mean(self):
    vectors = self.columnData()
    mean = Vector.mean(vectors)
    self.assertEqual([8/3, 3, 10/3], mean)

  @unittest.skip("unimplemented")
  def test_column_median(self):
    vectors = self.columnData()
    median = Vector.median(vectors)
    self.assertEqual([3,None,3], median)

  @unittest.skip("unimplemented")
  def test_row_stddev(self):
    vectors = self.columnData()
    stddevs = Vector.rowwiseStdDev(vectors)
    self.assertEqual([math.sqrt(2/3), math.sqrt(2/3), (1/3) * math.sqrt(38)], stddevs)

  @unittest.skip("unimplemented")
  def test_column_stddev(self):
    vectors = self.columnData()
    stddevs = Vector.stdDev(vectors)
    self.assertEqual([math.sqrt(14)/3, math.sqrt(2), math.sqrt(38)/3], stddevs)

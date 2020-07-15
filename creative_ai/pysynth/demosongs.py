# coding=utf-8

# Example 1: The C major scale
song1 = [
['c',4],['d',4],['e',4],['f',4],['g',4],['a',4],['b',4],['c5',2],['r',1],
['c3',4],['d3',4],['e3',4],['f3',4],['g3',4],['a3',4],['b3',4],['c4',2],['r',1],
['c1*', 1], ['c2*', 1], ['c3*', 1], ['c4*', 1], ['c5*', 1], ['c6*', 1], ['c7*', 1], ['c8*', 1],
]

# Example 2: Something a little more patriotic
song2 = (
  ('g', -8), ('e', 16),
  ('c*', 4), ('e', 4), ('g', 4),
  ('c5*', 2), ('e5', -8), ('d5', 16),
  ('c5*', 4), ('e', 4), ('f#', 4),
  ('g*', 2), ('g', 8), ('g', 8),
  ('e5*', -4), ('d5', 8), ('c5', 4),
  ('b*', 2), ('a', -8), ('b', 16),
  ('c5*', 4), ('c5', 4), ('g', 4),
  ('e*', 4), ('c', 4),
)

# Example 3: Beginning of Nocturne Op. 9 #2 by F. Chopin
song3 = (
  ('bb', 8),
  ('g5*', 2), ('f5', 8), ('g5', 8), ('f5', -4), ('eb5', 4), ('bb', 8),
  ('g5*', 4), ('c5', 8), ('c6', 4), ('g5', 8), ('bb5', -4), ('ab5', 4), ('g5', 8),
  ('f5*', -4), ('g5', 4), ('d5', 8), ('eb5', -4), ('c5', -4),
  ('bb*', 8), ('d6', 8), ('c6', 8), ('bb5', 16), ('ab5', 16), ('g5', 16), ('ab5', 16), ('c5', 16), ('d5', 16), ('eb5', -4),
)

# Example 4: J.S. Bach: Bourrée (from BWV 996)
song4_rh = (
  ('e', 8), ('f#', 8),
  ('g*', 4), ('f#', 8), ('e', 8), ('d#*', 4), ('e', 8), ('f#', 8),
  ('b3*', 4), ('c#', 8), ('d#', 8), ('e*', 4), ('d', 8), ('c', 8),
  ('b3*', 4), ('a3', 8), ('g3', 8), ('f#3*', 4), ('g3', 8), ('a3', 8),
  ('b3*', 8), ('a3', 8), ('g3', 8), ('f#3', 8), ('e3*', 4), ('e', 8), ('f#', 8),
  ('g*', 4), ('f#', 8), ('e', 8), ('d#*', 4), ('e', 8), ('f#', 8),
  ('b3*', 4), ('c#', 8), ('d#', 8), ('e*', 4), ('d', 8), ('c', 8),
  ('b3*', 4), ('a3', 8), ('g3', 8), ('g3*', 32), ('f#3*', 32), ('g3*', 32), ('f#3*', 32), ('g3*', 32), ('f#3*', 32), ('g3*', 32), ('f#3*', 6.4), ('g3', 8), ('g3*', -2),
)
# version without the trill:
#  ('b3*', 4), ('a3', 8), ('g3', 8), ('f#3*', -4), ('g3', 8), ('g3*', -2),

song4_lh = (
  ('g2', 8), ('f#2', 8),
  ('e2*', 4), ('a2', 4), ('b2', 4), ('a2', 4),
  ('g2*', 4), ('f#2', 4), ('e2', 4), ('f#2', 4),
  ('g2*', 4), ('a2', 4), ('b2', 4), ('a2', 4),
  ('g2*', 4), ('b2', 4), ('e2', 8), ('f#2', 8), ('g2', 8), ('f#2', 8),
  ('e2*', 4), ('a2', 4), ('b2', 4), ('a2', 4),
  ('g2*', 4), ('f#2', 4), ('e2', 4), ('f#2', 4),
  ('g2*', 4), ('c3', 4), ('d3', 4), ('d3', 4),
  ('b2*', -2),
)


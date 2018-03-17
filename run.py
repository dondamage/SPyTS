import SPyTS.TSAnalyser as TSA
import SPyTS.TSFileReader as TSFR

a = TSA.TSAnalyser()
f = TSFR.TSFileReader("./SPyTS/tmp/test_stream.ts")

for i in range(100):
  try:
    p = f.read()
    a.add_pkt(p)
  except Exception as e:
    print(e)


from snapsnare.system import ora

filename = None
print( ora.nvl(filename, 'test'))

filename = 'acme.wav'
print(ora.nvl(filename, 'test'))
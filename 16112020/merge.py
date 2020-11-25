
Def merge(x,y,z)

        df = x.merge(y, on = 'node', how = 'left')

        df = df.merge(z, on = 'node', how = 'left')

        df.dropna(axis = 0, how = 'any', inplace =True)

        return df
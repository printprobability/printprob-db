class ArrayDivideUtil:

    @classmethod
    def divide_into_chunks(cls, data, chunk_size=20):
        # looping till length l
        for i in range(0, len(data), chunk_size):
            yield data[i:i + chunk_size]

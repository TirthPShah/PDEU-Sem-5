import logging

logging.basicConfig(filename='metricsmultiplication.log',
                    level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def matrix_multiplication(A, B):
    logging.info("Starting matrix multiplication.")

    try:
        if not A or not B:
            raise ValueError("One or both matrices are empty.")

        if not all(len(row) == len(A[0]) for row in A):
            raise ValueError("Matrix A has inconsistent row lengths.")
        if not all(len(row) == len(B[0]) for row in B):
            raise ValueError("Matrix B has inconsistent row lengths.")

        n = len(A)     
        m = len(A[0]) 
        p = len(B)     
        q = len(B[0])  

        logging.debug(f"Dimensions of A: {n}x{m}")
        logging.debug(f"Dimensions of B: {p}x{q}")

        if m != p:
            raise ValueError(f"Dimension mismatch: A's columns ({m}) do not match B's rows ({p}).")

        logging.info("Matrix dimensions are valid for multiplication.")
        
        c = [[0 for i in range(q)] for j in range(n)]
        
        for i in range(n):  
            for j in range(q):  
                for k in range(m):  
                    c[i][j] += A[i][k] * B[k][j]
                    logging.debug(f"Updated c[{i}][{j}] to {c[i][j]} using A[{i}][{k}]={A[i][k]} and B[{k}][{j}]={B[k][j]}")
        logging.error(f"Error during matrix multiplication: {e}")
        
        logging.info("Matrix multiplication completed successfully.")
        return c

    except ValueError as e:
        logging.error(f"Error during matrix multiplication: {e}")
        return str(e)

    except Exception as e:
        logging.critical(f"Unexpected error: {e}")
        return "An unexpected error occurred."

a = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
b = [[1, 2, 3, 12], [4, 5, 6, 11], [7, 8, 9, 10]]

# Perform matrix multiplication and print the result
c = matrix_multiplication(a, b)
print(c)

import threading
import queue
import time

# Função para medir o tempo de execução
def timeit(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        return result, execution_time
    return wrapper

# Função executada por uma thread
@timeit
def worker(q, thread_num):
    start_time = time.time()  # Definindo o tempo de início dentro da função worker
    log_file = f"T{thread_num}.txt"
    with open(log_file, "w") as f:
        f.write(f"T{thread_num}:\n")
        f.write(f"Iniciando{thread_num}\n")
        items_processed = 0
        while True:
            item = q.get()
            if item is None:
                break
            try:
                items_processed += int(item)  # Tentar converter para inteiro
                f.write(f"Processando T-{thread_num} item:{item}\n")
            except ValueError:
                # Se não for possível converter para inteiro, ignorar e continuar
                f.write(f"Ignorando item não numérico: {item}\n")
            q.task_done()
        f.write(f"Morreu T-{thread_num}\n")
        f.write(f"Executou:{items_processed}\n")
        return items_processed, time.time() - start_time

# Função para ler o arquivo e colocar os itens na fila
@timeit
def read_file_and_enqueue(file_path, q):
    start_time = time.time()
    with open(file_path, "r") as file:
        chunk_size = 1000  # Tamanho do bloco de leitura
        while True:
            chunk = file.read(chunk_size)
            if not chunk:
                break
            lines = chunk.strip().split("\n")  # Dividir o chunk em linhas
            for line in lines:
                q.put(line)  # Adicionar cada linha à fila
    return None, time.time() - start_time

# Informar o arquivo a ser lido
file_path = input("Digite o caminho do arquivo a ser processado: ")

# Informar o número de threads
num_threads = int(input("Digite o número de threads: "))

# Criar uma fila
q = queue.Queue()

# Criar e iniciar as threads
threads = []
for i in range(num_threads):
    t = threading.Thread(target=worker, args=(q, i))
    t.start()
    threads.append(t)

# Ler o arquivo e adicionar partes à fila
_, read_time = read_file_and_enqueue(file_path, q)

# Esperar até que todas as partes sejam processadas
q.join()

# Adicionar um item especial para sinalizar o término
for i in range(num_threads):
    q.put(None)

# Esperar até que todas as threads terminem e coletar os resultados
total_sum = 0
processing_times = []
for t in threads:
    result = t.join()
    if result is not None:  # Verificar se o resultado não é None antes de desempacotar
        result, execution_time = result
        total_sum += result
        processing_times.append(execution_time)

# Verificar se há tempos de processamento antes de calcular o tempo máximo
if processing_times:
    max_processing_time = max(processing_times)
else:
    max_processing_time = 0

# Resultados
print("Resultado final da soma:", total_sum)
print("Tempo de leitura do arquivo:", read_time)

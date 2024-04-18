import threading
import queue

# Função executada por uma thread
def worker(q):
    while True:
        item = q.get()
        if item is None:
            break
        print("Processando item:", item)
        q.task_done()

# Criar uma fila
q = queue.Queue()

# Criar e iniciar a thread
t = threading.Thread(target=worker, args=(q,))
t.start()

# Adicionar itens à fila
for i in range(10):
    q.put(i)

# Esperar até que todos os itens sejam processados
q.join()

# Adicionar um item especial para sinalizar o término
q.put(None)
t.join()

<<<<<<< HEAD
=======
# FastAPI E-Commerce API
>>>>>>> e994edd (ORDERS router (put) updated)

## Installation & Running with Docker

### 1. Clone the repository

<<<<<<< HEAD
=======
* 🔐 JWT Authentication with user roles (admin/customer)
* 🛍️ Products with filtering, sorting, and pagination
* 🛒 Shopping carts
* 📦 Orders management
* 👤 User management
* 🎯 Query parameters for filtering
* ✅ Input validation with Pydantic
* 🛡️ Role-based access control

## Installation & Running with Docker

### 1. Clone the repository

>>>>>>> e994edd (ORDERS router (put) updated)
```bash
git clone https://github.com/salman415-462/dockerAPI
cd dockerAPI
```

### 2. Build the Docker image

```bash
docker build -t ecommerce-api .
```

### 3. Run the container

```bash
docker run -d -p 9000:9000 --name ecommerce_container ecommerce-api
```

### 4. Access the API

* 🌐 Main URL: [http://localhost:9000](http://localhost:9000)
* 📄 API Docs: [http://localhost:9000/docs](http://localhost:9000/docs)
* 🛒 Products: [http://localhost:9000/products/](http://localhost:9000/products/)

### 5. Stop the container when done

```bash
docker stop ecommerce_container
```

### 6. Remove the container (optional)

```bash
docker rm ecommerce_container
```

### 7. Restart the container later without rebuilding

```bash
docker start ecommerce_container
```

### 8. Check running containers

```bash
docker ps
```

### 9. Check all containers (including stopped)

```bash
docker ps -a
```

### 10. View container logs

```bash
docker logs ecommerce_container
```

> ⚠️ **Tip:** If the container name `ecommerce_container` is already in use, either remove it (`docker rm ecommerce_container`) or give a new name with `--name new_name`.

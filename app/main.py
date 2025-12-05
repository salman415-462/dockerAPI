from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import products, users, auth, carts, orders

app = FastAPI(
    title="E-Commerce API",
    version="1.0.0",
    docs_url="/docs",  # Keep docs accessible
    redoc_url="/redoc"
)

# CORS middleware - allow all origins for testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(products.router, prefix="/products", tags=["Products"])
app.include_router(carts.router, prefix="/carts", tags=["Carts"])
app.include_router(orders.router, prefix="/orders", tags=["Orders"])

@app.get("/")
async def root():
    return {
        "message": "Welcome to E-Commerce API",
        "docs": "/docs",
        "redoc": "/redoc",
        "status": "online"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "ecommerce-api"}

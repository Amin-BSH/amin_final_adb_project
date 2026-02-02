from fastapi import FastAPI
from routers import (
    ai,
    car,
    city,
    driver,
    province,
    user,
    village,
    farmer,
    factory,
    measure_unit,
    pesticide,
    payment_reason,
    crop_year,
    seed,
    carriage,
    carriage_status,
    commitment,
    factory_commitment_tonnage,
    factory_payment,
    factory_pesticide,
    factory_seed,
    factory_sugar,
    factory_waste,
    farmer_invoice_payed,
    farmers_guarantee,
    farmers_load,
    farmers_payment,
    farmers_pesticide,
    farmers_seed,
    farmers_sugar_delivery,
    farmers_waste_delivery,
    product,
    product_price,
    purity_price,
)

app = FastAPI(
    title="HavirKesht",
    description="Demo of havirkesht project",
)

# Routers
app.include_router(user.router)
app.include_router(ai.router)
app.include_router(province.router)
app.include_router(city.router)
app.include_router(village.router)
app.include_router(car.router)
app.include_router(driver.router)
app.include_router(farmer.router)
app.include_router(factory.router)
app.include_router(measure_unit.router)
app.include_router(pesticide.router)
app.include_router(payment_reason.router)
app.include_router(crop_year.router)
app.include_router(seed.router)
app.include_router(carriage.router)
app.include_router(carriage_status.router)
app.include_router(commitment.router)
app.include_router(factory_commitment_tonnage.router)
app.include_router(factory_payment.router)
app.include_router(factory_pesticide.router)
app.include_router(factory_seed.router)
app.include_router(factory_sugar.router)
app.include_router(factory_waste.router)
app.include_router(farmer_invoice_payed.router)
app.include_router(farmers_guarantee.router)
app.include_router(farmers_load.router)
app.include_router(farmers_payment.router)
app.include_router(farmers_pesticide.router)
app.include_router(farmers_seed.router)
app.include_router(farmers_sugar_delivery.router)
app.include_router(farmers_waste_delivery.router)
app.include_router(product.router)
app.include_router(product_price.router)
app.include_router(purity_price.router)

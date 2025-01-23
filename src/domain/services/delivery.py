__all__ = ("compute_orders_per_courier",)


def compute_orders_per_courier(
    *,
    delivery_orders_count: int,
    couriers_shift_duration: int,
) -> float:
    couriers_shift_duration_in_hours = couriers_shift_duration / 3600
    if couriers_shift_duration_in_hours == 0:
        return 0.0
    return delivery_orders_count / couriers_shift_duration_in_hours

function [active] = get_active(affinity, density, alpha, belta)
    active = alpha * affinity - belta * density;
    
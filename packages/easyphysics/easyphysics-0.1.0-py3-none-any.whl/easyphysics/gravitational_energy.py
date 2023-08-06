def gravitational_energy(m,h, g = 9.80665):
    
    
    """ calculate the energy possessed or acquired by an object due to a change in its position when it is present 
    in a gravitational field  = m*g*h

    Parameters
    ----------
    m : float
        A numeric value that is the mass of the object(kilograms).
    g : float, optional
       gravitational field 
    h: float
       height above the earth surface(metre).

    Returns
    -------
    ge : float
        A gravitational energy (float) value which is the energy stored in the object.

    Examples
    --------
    >>> gravitational_energy(2.5,10, g = 9.8)
    245.16
    >>> gravitational_energy(10,22, g = 9.80665)
    2157.463 
    """
    ge = m*g*h
    return ge 

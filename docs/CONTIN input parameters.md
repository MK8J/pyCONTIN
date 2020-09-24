# CONTIN input parameters

LAST
1: that last block of data
-1: not the last block of data


IUSER(4): for selecting the built-in kernel function USERK
1: For molecular weight distribution
2: diffusion coefficient distribution or Laplace transform
3: FOR SPHERICAL-RADIUS DISTRIBUTIONS
4: general form of kernel, need to modify the code of this part by the user (LINE 881)


 ```fortran
 USERK(T,G)=FORMF2(G)*G**RUSER(23)*EXP(-RUSER(21)*T*G**RUSER(22))
 ```


 NY format:

 5100 FORMAT (1H1,9X,80A1)

 5110 FORMAT (18H0(FOR ALPHA/S(1) =,1PE9.2,9H) PRUNS =,0PF7.4,9X,8HPUNCOR =,5F8.4)

 IFORMT a user-defined format specifier (defined in the input file)


# Parameters input format

5200 FORMAT (1X,6A1,I5,E15.6) --> This format is for parameters in input file
5210 FORMAT (/1X,6A1,I5,1PE15.5) --> This format is for the same set of parameters in output file


ORDINATE: xj or s(lambda)
ABSCISSA: lambda

IUSER(10)==1: molecular weight mode
default: $R_{23}=1$, $R_{21}=R_{18}*R_{20}^2$

IUSER(10)==2: Laplace transform
default: $R_{23}=0$, $R_{22}=1$, $R_{21}=R_{20}^2$

# Constrain the solution

1. Setting the number of peaks. See 4.1.6.4 of the manual or 4.7 in the main paper. Six parameters are for this: ```NNSGN```, ```NSGN```, ```LSIGN```, ```NFLAT```, ```SRMIN```, and ```MQPITR```.

2. Set quality and equality constraints. (see. CONTIN manual 4.1.2.5 and 4.1.2.6)
NEQ can be set in the setting FILE. But the matrix D, E in Eq. 3.6 and 3.7 should be set in the source code.

3. Set the weighting of each input data points using ```IWT```, or using ```IWT=4``` to manually set each point.


# Inputs for emission rate analysis

## The kernal

The kernel is the function value. For laplace we want $F = e^{-st}$

For laplace transform lambda is emission rates. Seems to work with R~22~ and R~23~ (set with RUSER) to -1, this means it fits time constant. I'm not sure if R~23~ should be zero or +-1. Though this maybe scalled by the amplitudes.

It strangley requires RUSER10 = 0, which means something to do with background.

$$F(\lambda_m, t_k) = f_m^2\lambda_m^{R_{23}} \exp\left(-R_{21}t_k\lambda_m^{R_{22}}\right)$$


The IFORMY and IFORMX. These a Fortran formatting codes. Number type, decimal length, number of "spaces", ect. See the above section on formatting.

The program works really well. If you manually try to calculate the amplitudes of the time constants you may find it does not. However, altering the input paramters provided to contin will alliviate this issue.

L3 should be False, as this makes $f_m==1$. I'm not sure what False is, is it a value of -1, 0 or 1?? Doesn't seem to change much.

N~g~ (NG) is number of output time constants! This is really the number of grid points. Defualt 31.


IUNIT is about saving computational time, through storing a large matrix.

## Background/Offset

This is controlled by N~L~ and L~k1~. Setting either to zero should turn this off.

## Weighting function

IWT is the weighting, and the number IWT is set to, is the power of y the standard deviation goes as. Default is 1. The following give the meaning of different values

* 1: is if the noise level for all data is the same level, i.e. doesn't depend on the expected y value.
* 2: if the noise follows possion
* 3: No idea
* 4: reads the values in
* 5: calls USERWT to calculate special cases.

NERFIT > 0, adds a condition to prevent small y values resulting in large error values, and dominating the fitting. This is set to 10, and is the number of points used.

## Regularisation

NORDER is the order of somethign or another

* 1 is good for ridge order extraction.
* 2 is good for smoothening

So NORDER = 2, for laplace. Default is 2.

NENDZ(J) determined the external boundy conditions, when NORDER >2. Higher values sets that number of rows to zero. (external grid points). Both are set to 2. Not sure really what this means.



## Peak finding.

Conitin only finds local peaks in s(lambda), as its not always good to find more.

## Outputs

CONTIN outputs many possible fits. It also highlights which fit it thinks is best.

DOUSOU = TRUE  gives more outputs
ONLY1 = False plots the solution and input!

A solution is considered good when:
  PROB1 TO REJECT less than about 0.9

## Simulating

simula = True will call USERSI and USEREX to produce simulated data.

## Other stuff

$c_m$ are the weights of the quadrature formula used for numerical integration.

IQUAD controls how c~m~ is calculated:

* 1: already in linear algebraice requations
* 2: trapezoidal
* 3: Simpson. default 3.

GMNMX (1) and (2) are the intervales of the integration (a --> b).
IGRID controls the quadrature grid:

* 1 is equal intervalues of lambda
* 2 is put the grid in equal intervalues of the monotonic function h(lambda) which is specified by USERTR. The defualt USERTR is ln(lambda).
* 3: c~m~ and lambda~m~ are not special. Defualt 2.

USERK evalues $F_k (\lambda_m)$.

NLINF. if equal N~L~, then USERLF is called to eval L. Default 0.

IUNIT >0, means F~k~ and L~k~ are writen to disk, in an effor to speed things up.

DOUSNQ == True, means USERNQ will set Nineq, D, and d. Its better for this is be False, if NONNEG is True. Default False.

NONNEG sets $N_{ineq} = N_g$, which means the amplitudes are can not be less than zero. Default True.

NEQ is the number of equalities that are set, the default is 0.

# Hints for inverting noisy Laplace tranforms

Hints for inverting noisy Laplace transforms described in the original source code.
```
Hints for inverting noisy Laplace transforms:
=============================================
With Laplace inversions, you might use the following Control
  Parameters:
    NONNEG=T (if the solution is known to be nonnegative; without
              this constraint the resolution is extremely poor.)
    IUSER(10)=2
    GMNMX(1) about 0.1/(maximum time value in your data of
                        signal vs. time)
    GMNMX(2) about 4/(time-spacing between data points at the
                      shortest times)
    NG about 12*log10[GMNMX(2)/GMNMX(1)]
    IFORMY, NINTT, etc., as appropriate for your data.

The CHOSEN SOLUTION gives you a conservative (smooth) estimate
  of a possible continuous distribution of exponentials.

The Reference Solution (the solution with the smallest ALPHA)
  gives you the optimal analysis as a discrete sum of
  exponentials.  The number of discrete exponentials is the
  number of peaks.  Each amplitude is given by MOMEMT(0) for
  the corresponding peak.  The decay rate constant is given by
  MOMENT(1)/MOMENT(0).

Choose the solution with the smallest ALPHA that has the same
  number of peaks as the CHOSEN SOLUTION.  This solution has
  less smoothing bias (smaller ALPHA), but still has about
  the same complexity (number of peaks) as the CHOSEN SOLUTION.
=================================================================
```

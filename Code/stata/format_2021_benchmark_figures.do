*******************************************************************************
* Purpose: Reformat the authors' 2021 Figures 7 and 9 for side-by-side slides.
* Author:  Lorenzo Gorini replication project
* Date:    2026-08-10
* Inputs:  MSS2021Febreplicationkit/data/finalfiles/
*          YinequalityFAanalysis.dta
* Outputs: Presentation/1_replication_package_validation/assets/
*          fig_nhhd_2021_presentation.{pdf,eps}
*          fig_safe_2021_presentation.{pdf,eps}
*
* Scope:   Formatting only. The variables, transformations, sample, signs,
*          normalization, colors, line patterns, and markers match the authors'
*          mss_analysis.do Figure 7 and Figure 9 blocks. Legends are moved into
*          the upper-left of the graph and the graph uses an 8:5 aspect ratio so
*          the plotting region is not compressed horizontally.
*******************************************************************************

clear all
set more off
set maxvar 32000

local project_root "`c(pwd)'"
local input_file "`project_root'/MSS2021Febreplicationkit/data/finalfiles/YinequalityFAanalysis.dta"
local output_dir "`project_root'/Presentation/1_replication_package_validation/assets"
local log_file "`project_root'/Presentation/1_replication_package_validation/logs/format_2021_benchmark_figures.log"

capture confirm file "`input_file'"
if _rc {
    display as error "Required input not found: `input_file'"
    exit 601
}

capture log close _all
log using "`log_file'", text replace

*******************************************************************************
* Figure 7: net household debt across the wealth distribution
*******************************************************************************

use "`input_file'", clear
isid year

foreach variable in fa896140001 a_hh1_hhd a_hh9_hhd a_hh90_hhd ///
    d_hh1_hhd d_hh9_hhd d_hh90_hhd a_hh1_hhdSZ a_hh9_hhdSZ ///
    a_hh90_hhdSZ d_hh1_hhdSZ d_hh9_hhdSZ d_hh90_hhdSZ {
    confirm variable `variable'
}

foreach num in 1 9 90 {
    replace d_hh`num'_hhd = -1 * d_hh`num'_hhd
    replace d_hh`num'_hhdSZ = -1 * d_hh`num'_hhdSZ
    generate n_hh`num'_hhd = a_hh`num'_hhd + d_hh`num'_hhd
    generate n_hh`num'_hhdSZ = a_hh`num'_hhdSZ + d_hh`num'_hhdSZ
}

foreach num in 1 9 90 {
    generate n_hh`num'_hhdSZ_2ni = n_hh`num'_hhdSZ / fa896140001
    summarize n_hh`num'_hhdSZ_2ni if year == 1982, meanonly
    if r(N) != 1 {
        display as error "Expected exactly one nonmissing 1982 observation for wealth group `num'."
        exit 459
    }
    local base_1982 = r(mean)
    generate n_hh`num'_hhdSZ_2ni_d = n_hh`num'_hhdSZ_2ni - `base_1982'
}

generate zero = 0

#delimit ;
graph twoway
    (scatter n_hh1_hhdSZ_2ni_d n_hh9_hhdSZ_2ni_d
        n_hh90_hhdSZ_2ni_d zero year,
        connect(l l l l)
        lpattern(solid dash longdash dash)
        lcolor(navy dkgreen maroon gray)
        lwidth(thick thick thick)
        msymbol(Dh Oh X i)
        mcolor(navy dkgreen maroon)),
    xlabel(1960(10)2020, labsize(medsmall))
    ylabel(-0.4(0.1)0.2, labsize(medsmall) format(%3.1f))
    ytitle("Scaled by NI, relative to 1982", size(medsmall))
    xtitle("")
    legend(order(1 "Top 1%" 2 "Next 9%" 3 "Bottom 90%")
        position(11) ring(0) rows(1) size(small)
        region(lcolor(none) fcolor(none)))
    graphregion(color(white))
    plotregion(margin(small))
    xsize(8) ysize(5)
    name(fig_nhhd_2021_presentation, replace);
#delimit cr

graph export "`output_dir'/fig_nhhd_2021_presentation.pdf", as(pdf) replace
graph export "`output_dir'/fig_nhhd_2021_presentation.eps", as(eps) replace
graph export "`output_dir'/fig_nhhd_2021_presentation.png", as(png) width(1600) replace

summarize n_hh1_hhdSZ_2ni_d n_hh9_hhdSZ_2ni_d n_hh90_hhdSZ_2ni_d ///
    if year == 2007
assert r(N) == 1

*******************************************************************************
* Figure 9: safe-asset demand by the rest of the world and top 1 percent
*******************************************************************************

use "`input_file'", clear
isid year

foreach variable in fa896140001 a_govd_tot a_hhd_tot a_row_hhd a_row_govd ///
    a_gov_hhd a_gov_govd a_oth_hhd a_oth_govd a_hh1_hhdSZ a_hh1_govdSZ ///
    a_hh9_hhdSZ a_hh9_govdSZ a_hh90_hhdSZ a_hh90_govdSZ {
    confirm variable `variable'
}

generate a_hh99_hhdSZ = a_hh9_hhdSZ + a_hh90_hhdSZ
generate a_hh99_govdSZ = a_hh9_govdSZ + a_hh90_govdSZ
generate a_demd_tot = a_govd_tot + a_hhd_tot

foreach holder in row gov oth {
    generate a_`holder'_demd = a_`holder'_hhd + a_`holder'_govd
}

foreach num in 1 9 90 99 {
    generate a_hh`num'_demdSZ = a_hh`num'_govdSZ + a_hh`num'_hhdSZ
}

sort year
generate a_row_demd2ni = a_row_demd / fa896140001
generate a_hh1_demdSZ2ni = a_hh1_demdSZ / fa896140001

#delimit ;
graph twoway
    (scatter a_row_demd2ni a_hh1_demdSZ2ni year,
        connect(l l)
        lpattern(solid dash)
        lcolor(purple navy)
        lwidth(thick thick)
        msymbol(Dh Oh)
        mcolor(purple navy)),
    xlabel(1960(10)2020, labsize(medsmall))
    ylabel(0(0.1)0.6, labsize(medsmall) format(%3.1f))
    ytitle("Scaled by NI", size(medsmall))
    xtitle("")
    legend(order(1 "Rest of world" 2 "Top 1%")
        position(11) ring(0) rows(1) size(small)
        region(lcolor(none) fcolor(none)))
    graphregion(color(white))
    plotregion(margin(small))
    xsize(8) ysize(5)
    name(fig_safe_2021_presentation, replace);
#delimit cr

graph export "`output_dir'/fig_safe_2021_presentation.pdf", as(pdf) replace
graph export "`output_dir'/fig_safe_2021_presentation.eps", as(eps) replace
graph export "`output_dir'/fig_safe_2021_presentation.png", as(png) width(1600) replace

count if !missing(a_row_demd2ni, a_hh1_demdSZ2ni)
assert r(N) > 0

log close

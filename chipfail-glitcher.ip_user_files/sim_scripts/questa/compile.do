vlib questa_lib/work
vlib questa_lib/msim

vlib questa_lib/msim/xil_defaultlib
vlib questa_lib/msim/xpm

vmap xil_defaultlib questa_lib/msim/xil_defaultlib
vmap xpm questa_lib/msim/xpm

vlog -work xil_defaultlib -64 -sv "+incdir+../../ipstatic" \
"D:/Xilinx/Vivado/2019.1/data/ip/xpm/xpm_cdc/hdl/xpm_cdc.sv" \

vcom -work xpm -64 -93 \
"D:/Xilinx/Vivado/2019.1/data/ip/xpm/xpm_VCOMP.vhd" \

vlog -work xil_defaultlib -64 "+incdir+../../ipstatic" \
"C:/Users/Nhan Nguyen/Downloads/chipfail-glitcher-master/chipfail-glitcher.srcs/sources_1/ip/clk_wiz_0/clk_wiz_0_clk_wiz.v" \
"C:/Users/Nhan Nguyen/Downloads/chipfail-glitcher-master/chipfail-glitcher.srcs/sources_1/ip/clk_wiz_0/clk_wiz_0.v" \
"C:/Users/Nhan Nguyen/Downloads/chipfail-glitcher-master/chipfail-glitcher.srcs/sources_1/new/delay.v" \
"C:/Users/Nhan Nguyen/Downloads/chipfail-glitcher-master/chipfail-glitcher.srcs/sources_1/new/pulse.v" \
"C:/Users/Nhan Nguyen/Downloads/chipfail-glitcher-master/chipfail-glitcher.srcs/sources_1/new/top.v" \
"C:/Users/Nhan Nguyen/Downloads/chipfail-glitcher-master/chipfail-glitcher.srcs/sources_1/new/trigger.v" \
"C:/Users/Nhan Nguyen/Downloads/chipfail-glitcher-master/chipfail-glitcher.srcs/sources_1/new/uart_rx.v" \
"C:/Users/Nhan Nguyen/Downloads/chipfail-glitcher-master/chipfail-glitcher.srcs/sources_1/new/uart_tx.v" \
"C:/Users/Nhan Nguyen/Downloads/chipfail-glitcher-master/chipfail-glitcher.srcs/sources_1/new/uint32_receiver.v" \

vlog -work xil_defaultlib \
"glbl.v"


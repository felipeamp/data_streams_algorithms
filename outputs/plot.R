ams.df <- read.csv('benchmark_ams_surprisenumber.csv')

ams.df <- data.frame('surprise-number' = c(3387741298432, 21359998.8, 55179996.9, 328872781.52, 3265513056.54), 'average-time' = c(8.4e-3, 6.18e-5, 1.1e-4, 4.01e-4, 2.91e-3), 'total-time' = c(8.4e-3, 1.1e2, 1.99e3, 7.19e3, 5.18e4), 'num-samples' = c(1, 10, 100, 1000, 10000))

svg('plot.svg', width = 8, height = 8)

par(mar = c(5,5,2,5));
with(ams.df, plot(x = c(0, log(Num.Samples, base=10)),
                  y = c(Exact.Proc.Time[1], AMS.Avg.Proc.Time),
                  type = 'l',
                  col = 'red3',
                  xlab = expression(log[10](italic('Number of Samples'))),
                  ylab = 'Average time'))

with(ams.df, points(x = c(0, log(Num.Samples, base=10)),
                    y = c(Exact.Proc.Time[1], AMS.Avg.Proc.Time),
                    col = 'red3',
                    pch = 8))

par(new = T)
with(ams.df, plot(x = c(0, log(Num.Samples, base=10)),
                  y = log(c(Exact.SN[1], AMS.SN), base=10),
                  type = 'p',
                  col = 'black',
                  xlab = NA,
                  ylab = NA,
                  pch = 16,
                  axes = F,
                  cex = 1.2))

axis(side = 4)
mtext(side = 4, line = 3, text = expression(log[10](italic('Surprise Number'))))
legend('topright',
       legend = c('Time (s)', 'Surprise number'),
       col = c('red3', 'black'),
       lty = c(1, 0),
       pch = c(8, 16))

dev.off()

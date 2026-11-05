# YSF2DMR bridge / 桥接

Configure YSF and YSF2DMR in Pi-Star, Apply Changes, then use Yaesu System Fusion Configuration: YSF startup host00002/Link YSF2DMR, your valid DMR ID, intended master, Hotspot Security and target TG. Never publish the password. DG-ID0 and five-digit YSF rooms are not DMR TGs.

Pi-Star开启YSF及YSF2DMR并应用后，在八重洲配置区选择00002/Link YSF2DMR，配置本人有效ID、目标主站、密码与TG；DG0不等于DMR组号。测试本机桥时不要连接其他反射器。手台RX必须对应热点TX，手台TX对应热点RX。

Verify with an independent network receiver/Hoseline. A local tail echo proves no remote TG delivery. Check RF header/end, gateway/master login and network route separately; redact IDs/IP/passwords before sharing logs.
用独立接收端核对真实交付；本地尾音回声不能证明进入目标TG。分别检查RF收发、网关登录和网络路由，日志先去除私人信息。

[Operating guide / 操作说明](C4FM_OPERATING.en.md)

# 烧录站自动发布

站点：https://opengd77-digiall.pages.dev/ 。使用现有 Pages 项目 `opengd77-digiall`，由公开仓库的 GitHub Actions 自动部署，私有固件源码不进入站点。

## 一次性配置

在本公开仓库 **Settings → Secrets and variables → Actions → New repository secret** 添加：

- `CLOUDFLARE_ACCOUNT_ID`：现有 Pages 项目所属账号的 Account ID。
- `CLOUDFLARE_API_TOKEN`：限定该账号、具有 **Account → Cloudflare Pages → Edit** 权限的 API Token。

不要把 Token 放入聊天、仓库文件、网页脚本或 Actions 日志。流水线读取现有项目的生产分支，不假设它叫 main，也不创建或替换项目。

配置后，打开 [Deploy verified firmware site 工作流](https://github.com/xunyu5800-alt/OpenGD77-DIGIALL-Testing/actions/workflows/deploy-pages.yml)，点击 **Run workflow**，选择 main，tag 留空，即可首次同步最新已发布固件。无需手动上传 ZIP。

## 后续发布

发布固件 Release（包括 rc 公测版）后自动更新。使用 `GITHUB_TOKEN` 的发布流水线应保留工作流显示名称 **Publish verified firmware**；部署通过其成功结束的 `workflow_run` 事件启动，避免 Release 事件不触发下游流水线的问题。当前 rc.17 的旧名称也兼容。人工发布 Release、main 上的页面修改也会触发部署。

自动任务按 published_at 选择带 `release_manifest.json` 的最新已发布固件，包含 prerelease，排除草稿及独立刷机工具 Release。较早的排队事件仍选当前最新版本。新版本沿用发布清单格式：六个原生板型、各含 font/pinyin/main，提供 SHA256SUMS.txt 和来源提交。

部署前逐一验证清单、六个机型 ZIP、内部固件大小/摘要/来源和空编解码器区域；保留并校验现有上游参考包。ZIP 改成同域名版本目录，页面版本和机型数据一起部署。校验失败不会发起 Cloudflare 部署。部署后再从生产域名回读机型列表和每个 ZIP 的实际字节。

每次运行保留 7 天 `verified-pages-site` 构建产物。站点 `/deployment-version.json` 记录发布版本、固件来源、文档提交和下载摘要。目录/页面要求重新验证缓存，版本化下载长期缓存。

## 回滚和排错

手动运行上述工作流，在 tag 填入一个具有兼容发布清单的旧版本，可原子回滚整站；后续自动发布仍会选择最新版本。仅重新运行任务不会修改 GitHub 已发布固件。

缺少 Secret 或权限时，在读取 Pages 项目的步骤明确失败，既有站点继续服务。补齐后重新运行即可。若项目已启用 Cloudflare Git 自动构建，应在 Cloudflare 关闭其自动生产部署，统一使用此工作流，避免未经资产准备的 docs 目录覆盖同域名 ZIP。

本地验证（Python 3.12，无第三方依赖）：

```console
python .github/scripts/test_pages_site.py
python .github/scripts/pages_site.py build
```

`build` 下载并验证公开包，输出全新 `.site-build` 目录；已有输出时拒绝覆盖。可另传 `--output`。它不调用烧录设备。

官方说明：[Cloudflare Pages 持续集成部署](https://developers.cloudflare.com/pages/how-to/use-direct-upload-with-continuous-integration/)、[GitHub Token 触发限制](https://docs.github.com/en/actions/concepts/security/github_token)。

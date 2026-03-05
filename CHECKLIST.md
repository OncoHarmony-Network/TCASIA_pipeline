# TCASIA GitHub Repository Checklist

## ✅ 已完成的内容

### 核心文档
- [x] README.md - 项目主文档
- [x] LICENSE - MIT 许可证
- [x] CITATION.md - 引用信息
- [x] CONTRIBUTING.md - 贡献指南

### 详细文档 (docs/)
- [x] installation.md - 安装指南
- [x] usage.md - 使用教程
- [x] parameters.md - 参数参考
- [x] output_format.md - 输出格式说明

### 工作流文件
- [x] workflows/01_alignment/ - 比对工作流
  - [x] Snakefile
  - [x] README.md
  - [x] config/config.yml (示例)
  - [x] config/config.template.yml (模板)
  - [x] envs/*.yaml (Conda 环境)
- [x] workflows/02_as_calling/ - AS 检测工作流
  - [x] Snakefile
  - [x] README.md
  - [x] config/config.yml (示例)
  - [x] config/config.template.yml (模板)
  - [x] envs/*.yaml (Conda 环境)
  - [x] rules/*.smk (规则文件)

### 配置文件
- [x] .env.example - 环境变量模板
- [x] .gitignore - Git 忽略规则

---

## ⚠️ 需要补充的内容

### 1. 文档文件 (高优先级)

#### docs/troubleshooting.md
**状态**: ❌ 缺失
**重要性**: ⭐⭐⭐⭐⭐
**内容**: 常见问题和解决方案
- 安装问题
- 运行错误
- 性能优化
- 数据质量问题

#### docs/examples.md
**状态**: ❌ 缺失
**重要性**: ⭐⭐⭐⭐
**内容**: 实际使用案例
- 完整的示例数据集
- 端到端运行示例
- 结果解读示例

#### METHOD_VERIFICATION.md
**状态**: ❌ 缺失 (README 中提到)
**重要性**: ⭐⭐⭐⭐⭐
**内容**: 代码-方法一致性报告
- 参数验证
- 算法实现验证
- 与论文方法的对应关系

### 2. 脚本文件

#### scripts/read_length.sh
**状态**: ❌ 缺失 (文档中多次引用)
**重要性**: ⭐⭐⭐⭐⭐
**功能**: 检测 FASTQ/BAM 文件的读长
```bash
#!/bin/bash
# 用法: bash read_length.sh <input.bam>
```

#### scripts/check_strandness.sh
**状态**: ❌ 建议添加
**重要性**: ⭐⭐⭐⭐
**功能**: 使用 RSeQC 检测链特异性

#### scripts/validate_config.py
**状态**: ❌ 建议添加
**重要性**: ⭐⭐⭐
**功能**: 验证配置文件的正确性

### 3. 测试文件

#### tests/ 目录
**状态**: ❌ 完全缺失
**重要性**: ⭐⭐⭐⭐
**内容**:
- tests/data/ - 测试数据
- tests/config/ - 测试配置
- tests/run_tests.sh - 测试脚本
- tests/README.md - 测试说明

### 4. 示例数据

#### examples/ 目录
**状态**: ❌ 缺失
**重要性**: ⭐⭐⭐
**内容**:
- examples/small_dataset/ - 小型示例数据集
- examples/config/ - 示例配置文件
- examples/expected_output/ - 预期输出
- examples/README.md - 示例说明

### 5. GitHub 特定文件

#### .github/workflows/
**状态**: ❌ 缺失
**重要性**: ⭐⭐⭐
**内容**: GitHub Actions CI/CD
- .github/workflows/test.yml - 自动化测试
- .github/workflows/lint.yml - 代码检查

#### .github/ISSUE_TEMPLATE/
**状态**: ❌ 缺失
**重要性**: ⭐⭐⭐
**内容**: Issue 模板
- bug_report.md
- feature_request.md

#### .github/PULL_REQUEST_TEMPLATE.md
**状态**: ❌ 缺失
**重要性**: ⭐⭐⭐
**内容**: PR 模板

### 6. 其他重要文件

#### CHANGELOG.md
**状态**: ❌ 缺失
**重要性**: ⭐⭐⭐⭐
**内容**: 版本更新日志

#### CONTRIBUTORS.md
**状态**: ❌ 缺失
**重要性**: ⭐⭐
**内容**: 贡献者列表

#### CODE_OF_CONDUCT.md
**状态**: ❌ 缺失
**重要性**: ⭐⭐
**内容**: 行为准则

---

## 🔧 需要修改的内容

### 1. 更新 README.md
- [ ] 替换 `YOUR_USERNAME` 为实际的 GitHub 用户名
- [ ] 添加实际的 DOI (发表后)
- [ ] 更新仓库 URL

### 2. 更新所有文档中的占位符
- [ ] GitHub 仓库链接
- [ ] 联系邮箱确认
- [ ] 作者信息

### 3. 清理配置文件
- [ ] 确保 config.yml 不包含敏感路径
- [ ] 验证 config.template.yml 的通用性

### 4. 验证环境文件
- [ ] 检查所有 .yaml 文件的依赖版本
- [ ] 确保跨平台兼容性

---

## 📋 发布前检查清单

### 代码质量
- [ ] 所有 Snakefile 通过 `--lint` 检查
- [ ] 配置模板文件无硬编码路径
- [ ] 脚本文件有执行权限
- [ ] 代码注释完整

### 文档完整性
- [ ] 所有文档链接有效
- [ ] 示例命令可执行
- [ ] 参数说明准确
- [ ] 故障排除指南完整

### 安全性
- [ ] .gitignore 包含所有敏感文件
- [ ] 无硬编码密码或密钥
- [ ] MAJIQ 许可证不在仓库中
- [ ] 示例配置使用占位符

### 可用性
- [ ] README 清晰易懂
- [ ] 安装步骤可复现
- [ ] 示例数据可访问
- [ ] 错误信息有帮助

### 社区
- [ ] 贡献指南完整
- [ ] Issue 模板设置
- [ ] PR 模板设置
- [ ] 许可证明确

---

## 🚀 建议的发布流程

### 阶段 1: 核心功能 (v0.1.0)
1. 完成所有高优先级文档 (⭐⭐⭐⭐⭐)
2. 添加 read_length.sh 脚本
3. 创建 METHOD_VERIFICATION.md
4. 更新所有占位符

### 阶段 2: 测试和示例 (v0.2.0)
1. 添加测试框架
2. 提供小型示例数据集
3. 完善故障排除文档

### 阶段 3: 社区功能 (v1.0.0)
1. 设置 GitHub Actions
2. 添加 Issue/PR 模板
3. 创建 CHANGELOG.md
4. 发布正式版本

---

## 📝 立即行动项

### 最高优先级 (今天完成)
1. ✅ 创建 .env.example
2. ✅ 创建 .gitignore
3. ✅ 完成核心文档 (installation, usage, parameters, output_format)
4. ✅ 创建 CONTRIBUTING.md
5. ⏳ 创建 METHOD_VERIFICATION.md
6. ⏳ 创建 scripts/read_length.sh
7. ⏳ 更新 README 中的占位符

### 高优先级 (本周完成)
1. ⏳ 创建 docs/troubleshooting.md
2. ⏳ 创建 CHANGELOG.md
3. ⏳ 添加基础测试
4. ⏳ 验证所有配置模板

### 中优先级 (发布前完成)
1. ⏳ 创建示例数据集
2. ⏳ 设置 GitHub Actions
3. ⏳ 添加 Issue/PR 模板
4. ⏳ 创建 CODE_OF_CONDUCT.md

---

## 💡 额外建议

### 1. 版本管理
使用语义化版本 (Semantic Versioning):
- v0.x.x: 开发版本
- v1.0.0: 首个稳定版本
- v1.x.x: 向后兼容的更新
- v2.0.0: 重大变更

### 2. 发布策略
- 在 GitHub 创建 Release
- 使用 Zenodo 获取 DOI
- 在 Bioconda 发布 (可选)
- 在 WorkflowHub 注册 (可选)

### 3. 文档托管
考虑使用:
- GitHub Pages (简单)
- Read the Docs (专业)
- MkDocs (现代化)

### 4. 社区建设
- 创建 Discussions 板块
- 设置 Wiki (可选)
- 添加 Twitter/社交媒体链接
- 创建 Slack/Discord 频道 (可选)

---

## 📞 联系方式

如有问题，请联系:
- **Email**: jianguo.zhou@zmu.edu.cn
- **GitHub**: 待更新

---

**最后更新**: 2026-03-03
**状态**: 核心文档已完成，需要补充测试和示例

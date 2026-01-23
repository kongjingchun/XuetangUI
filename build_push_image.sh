#!/usr/bin/env bash
set -euo pipefail

# 默认配置
DEFAULT_REPO="xuetangx-registry.cn-beijing.cr.aliyuncs.com/xc-project/xc/xc-autotest-ui"
DEFAULT_PLATFORMS="linux/amd64,linux/arm64"
BUILDX_BUILDER="multiarch-builder"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印带颜色的消息
info() { echo -e "${BLUE}ℹ${NC} $1"; }
success() { echo -e "${GREEN}✅${NC} $1"; }
warning() { echo -e "${YELLOW}⚠${NC} $1"; }
error() { echo -e "${RED}❌${NC} $1" >&2; }

# 显示帮助信息
show_help() {
    cat << EOF
用法: $0 [选项]

选项:
  -r, --repo REPO        镜像仓库地址 (默认: ${DEFAULT_REPO})
  -t, --tag TAG          镜像标签 (默认: 时间戳 YYYYMMDDHHMM)
  -p, --platform PLAT    目标平台，逗号分隔 (默认: ${DEFAULT_PLATFORMS})
  -l, --latest           同时打 latest 标签
  -b, --build-only       仅构建，不推送
  -c, --no-cache         不使用构建缓存
  -h, --help             显示此帮助信息

示例:
  $0                                    # 使用默认配置构建并推送
  $0 -t v1.0.0 -l                       # 构建 v1.0.0 标签并同时打 latest
  $0 -p linux/amd64 -b                  # 仅构建 amd64 平台，不推送
  $0 -r my-registry.com/image -t dev    # 使用自定义仓库和标签
EOF
}

# 解析命令行参数
REMOTE_REPO="${DEFAULT_REPO}"
TAG=""
PLATFORMS="${DEFAULT_PLATFORMS}"
TAG_LATEST=false
BUILD_ONLY=false
NO_CACHE=false

while [[ $# -gt 0 ]]; do
    case $1 in
        -r|--repo)
            REMOTE_REPO="$2"
            shift 2
            ;;
        -t|--tag)
            TAG="$2"
            shift 2
            ;;
        -p|--platform)
            PLATFORMS="$2"
            shift 2
            ;;
        -l|--latest)
            TAG_LATEST=true
            shift
            ;;
        -b|--build-only)
            BUILD_ONLY=true
            shift
            ;;
        -c|--no-cache)
            NO_CACHE=true
            shift
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            error "未知参数: $1"
            show_help
            exit 1
            ;;
    esac
done

# 如果没有指定标签，使用时间戳
if [[ -z "$TAG" ]]; then
    TAG=$(date +"%Y%m%d%H%M")
fi

# 检查 Docker 是否安装
if ! command -v docker &> /dev/null; then
    error "Docker 未安装或不在 PATH 中"
    exit 1
fi

# 检查 Docker 是否运行
if ! docker info &> /dev/null; then
    error "Docker daemon 未运行"
    exit 1
fi

# 检查并设置 buildx
info "检查 Docker Buildx..."
if ! docker buildx version &> /dev/null; then
    error "Docker Buildx 不可用，请升级 Docker 或安装 buildx 插件"
    exit 1
fi

# 创建或使用 buildx builder
if ! docker buildx inspect "${BUILDX_BUILDER}" &> /dev/null; then
    info "创建 buildx builder: ${BUILDX_BUILDER}"
    docker buildx create --name "${BUILDX_BUILDER}" --use --bootstrap || {
        warning "创建 builder 失败，使用默认 builder"
        BUILDX_BUILDER="default"
    }
else
    info "使用现有 buildx builder: ${BUILDX_BUILDER}"
    docker buildx use "${BUILDX_BUILDER}"
fi

# 构建标签列表
TAGS=("${REMOTE_REPO}:${TAG}")
if [[ "$TAG_LATEST" == true ]]; then
    TAGS+=("${REMOTE_REPO}:latest")
fi

# 构建 tag 参数
TAG_ARGS=()
for tag in "${TAGS[@]}"; do
    TAG_ARGS+=("--tag" "$tag")
done

# 构建参数
BUILD_ARGS=(
    "buildx" "build"
    "--platform" "${PLATFORMS}"
    "${TAG_ARGS[@]}"
)

if [[ "$BUILD_ONLY" == false ]]; then
    BUILD_ARGS+=("--push")
else
    BUILD_ARGS+=("--load")
    # --load 只支持单平台
    if [[ "$PLATFORMS" == *","* ]]; then
        warning "--load 模式只支持单平台，将使用第一个平台: ${PLATFORMS%%,*}"
        BUILD_ARGS[2]="--platform"
        BUILD_ARGS[3]="${PLATFORMS%%,*}"
    fi
fi

if [[ "$NO_CACHE" == true ]]; then
    BUILD_ARGS+=("--no-cache")
fi

BUILD_ARGS+=(".")

# 显示构建信息
echo ""
info "构建配置:"
echo "  仓库: ${REMOTE_REPO}"
echo "  标签: ${TAG}${TAG_LATEST:+ (同时打 latest)}"
echo "  平台: ${PLATFORMS}"
echo "  模式: $([ "$BUILD_ONLY" == true ] && echo "仅构建" || echo "构建并推送")"
echo "  缓存: $([ "$NO_CACHE" == true ] && echo "禁用" || echo "启用")"
echo ""

# 执行构建
info "开始构建 Docker 镜像..."
if docker "${BUILD_ARGS[@]}"; then
    echo ""
    success "构建完成！"
    for tag in "${TAGS[@]}"; do
        success "  ${tag}"
    done
else
    echo ""
    error "构建失败"
    exit 1
fi

# 中国分省食辣偏好地图

把本文件夹里的 `china-province-spicy-preference.geojson` 拖进[凌波微图（NimbleMap）](https://nimblemap.com/zh/download.html)，地图会自动打开。也可以在浏览器里使用 [nimblemap.app](https://nimblemap.app/)。文件不会离开你的电脑。

本数据集托管在凌波微图网站上，可直接下载：

- [打包文件（GeoJSON、CSV 和本说明）](https://nimblemap.com/data/china-province-spicy-preference/china-province-spicy-preference.zip)
- [GeoJSON](https://nimblemap.com/data/china-province-spicy-preference/china-province-spicy-preference.geojson)
- [CSV](https://nimblemap.com/data/china-province-spicy-preference/china-province-spicy-preference.csv)

## 字段

- `spiciness_score`：食辣偏好评分，1 最淡，10 最辣。台湾、香港、澳门在原论文中没有数据，此栏为空。
- `diet_area`：原论文的三组划分。中文作「重辣 / 偏淡 / 稍辣」。请注意：论文英文把沿海低分组叫做 Mildly-spicy，把北方和西部的中低分组叫做 Slightly-spicy，和中文习惯不完全对应。看图和比较省份时，请以 1–10 的评分为准。
- `diet_area_en`：论文原文组名。
- `name` / `name_short` / `adcode`：省级行政区名称和代码。

## 资料来源与限度

评分来自 Zou, Ziying 与 Zou, Xuexiao，2021，《Geographical and Ecological Differences in Pepper Cultivation and Consumption in China》，*Frontiers in Nutrition* 8:718517，[doi: 10.3389/fnut.2021.718517](https://doi.org/10.3389/fnut.2021.718517)，表 4。原数据由国家特色蔬菜产业技术体系组织的问卷、调查和专家评分汇总。

这是近年的食辣偏好，不是清代「以辣代盐」的历史分布，也不是人均辣椒消费量。2021 年 Bromham 等人发表在 *Nature Human Behaviour* 的文章没有中国分省或县级辣度地图；他们的中国数据统计的是菜谱里香辛料的种类数，不是辣度。

没有找到可靠的公开县级吃辣度数据，因此这里不做县图，也不用省数据插值到县。

本文件中的省级行政区边界来自阿里云 DataV.GeoAtlas。底图为示意图，边界不作为划界依据。

## 文件

- `china-province-spicy-preference.geojson`：主数据，可直接拖进凌波微图
- `china-province-spicy-preference.csv`：同一套属性表
- `china-province-spicy-preference.zip`：上述两个文件和本说明的打包下载

---

# China's provincial spicy-preference map

Drag `china-province-spicy-preference.geojson` into [NimbleMap](https://nimblemap.com/download.html), or open it in the browser at [nimblemap.app](https://nimblemap.app/). The file stays on your computer.

Direct downloads:

- [Zip (GeoJSON, CSV, and this README)](https://nimblemap.com/data/china-province-spicy-preference/china-province-spicy-preference.zip)
- [GeoJSON](https://nimblemap.com/data/china-province-spicy-preference/china-province-spicy-preference.geojson)
- [CSV](https://nimblemap.com/data/china-province-spicy-preference/china-province-spicy-preference.csv)

## Fields

- `spiciness_score`: spicy-preference score, 1 = mildest, 10 = spiciest. Taiwan, Hong Kong and Macao have no scores in the source paper, so this field is empty for those units.
- `diet_area`: the paper's three-group labels, given here in Chinese (重辣 / 偏淡 / 稍辣). The paper's English names do not map neatly onto ordinary Chinese usage: the low-scoring coastal group is called Mildly-spicy, and the mid-to-low northern and western group is called Slightly-spicy. When you colour or compare provinces, use the 1–10 scores.
- `diet_area_en`: the paper's original group names.
- `name` / `name_short` / `adcode`: province-level names and codes.

## Sources and limits

Scores are from Zou, Ziying and Zou, Xuexiao, 2021, “Geographical and Ecological Differences in Pepper Cultivation and Consumption in China”, *Frontiers in Nutrition* 8:718517, [doi: 10.3389/fnut.2021.718517](https://doi.org/10.3389/fnut.2021.718517), Table 4. The original figures were compiled from questionnaires, surveys and expert scores organised by China's national specialty vegetable industry technology system.

This is recent preference, not the Qing-era history of substituting chilli for salt, and not per-capita chilli consumption. Bromham et al. (2021, *Nature Human Behaviour*) did not publish a provincial or county heat map of spiciness in China; their China data count the number of spice types in recipes, not heat.

No reliable public county-level spiciness data was found, so this release has no county map and does not interpolate provincial scores to counties.

Province boundaries in this GeoJSON come from Alibaba Cloud DataV.GeoAtlas. The basemap is schematic and is not a boundary authority.

## Files

- `china-province-spicy-preference.geojson`: the main file; drag it into NimbleMap
- `china-province-spicy-preference.csv`: the same attribute table
- `china-province-spicy-preference.zip`: those two files plus this README

<template>
  <div class="gantt-chart" ref="ganttChart">
    <g-gantt-chart style="width: 100%;" :row-height="ganttChartRowHeight" date-format="YYYY-MM-DD"
      chart-start="2025-01-01" chart-end="2025-07-31" precision="week" bar-start="myBeginDate" bar-end="myEndDate" color-scheme="vue">
      <g-gantt-row v-for="rowBar in rowBarList" immobile="true" :label="rowBar.title" :bars="rowBar.bars"
        :key="rowBar.title" />
    </g-gantt-chart>
  </div>
</template>

<script setup>
import { onMounted, ref, useTemplateRef } from "vue"

const ganttChartRef = useTemplateRef("ganttChart")
const ganttChartRowHeight = ref(100)
const rowBarList = ref(
  [
    {
      title: "Frontend development",
      bars: [
        {
          myBeginDate: "2025-02-01",
          myEndDate: "2025-04-07",
          ganttBarConfig: {
            // each bar must have a nested ganttBarConfig object ...
            id: "frontend-1", // ... and a unique "id" property
            label: "framework",
            immobile: true,
            hasHandles: true,
            style: {
              // arbitrary CSS styling for your bar
              background: "#5f9ea0",
              borderRadius: "20px",
              color: "black",
              fontSize: "10px"
            }
          }
        }
      ]
    },
    {
      title: "End Application development",
      bars: [
        {
          myBeginDate: "2025-03-15",
          myEndDate: "2025-05-05",
          ganttBarConfig: {
            id: "end-1",
            hasHandles: true,
            label: "Build End App in PC",
            immobile: true,
            style: {
              // arbitrary CSS styling for your bar
              background: "#5f9ea0",
              borderRadius: "20px",
              color: "black",
              fontSize: "10px"

            }
          }
        }
      ]
    },
    {
      title: "Backend development",
      bars: [
        {
          myBeginDate: "2025-02-15",
          myEndDate: "2025-05-05",
          ganttBarConfig: {
            id: "backend-1",
            hasHandles: true,
            label: "Build End App in PC",
            immobile: true,
            style: {
              // arbitrary CSS styling for your bar
              background: "#5f9ea0",
              borderRadius: "20px",
              color: "black",
              fontSize: "10px"

            }
          }
        }
      ]
    },
    {
      title: "Fine-tuning model with datasets",
      bars: [
        {
          myBeginDate: "2025-02-15",
          myEndDate: "2025-05-20",
          ganttBarConfig: {
            id: "model-1",
            hasHandles: true,
            label: "Fine-tuning model with datasets",
            immobile: true,
            style: {
              // arbitrary CSS styling for your bar
              background: "#5f9ea0",
              borderRadius: "20px",
              color: "black",
              fontSize: "10px"

            }
          }
        }
      ]
    },
    {
      title: "Interim Report",
      bars: [
        {
          myBeginDate: "2025-05-01",
          myEndDate: "2025-06-01",
          ganttBarConfig: {
            id: "interimreport-1",
            hasHandles: true,
            label: "Interim Report",
            immobile: true,
            style: {
              // arbitrary CSS styling for your bar
              background: "#5f9ea0",
              borderRadius: "20px",
              color: "black",
              fontSize: "10px"
            }
          }
        }
      ]
    },
    {
      title: "Deploy a Multi-Agent Architecture",
      bars: [
        {
          myBeginDate: "2025-06-01",
          myEndDate: "2025-07-07",
          ganttBarConfig: {
            id: "multiangent-1",
            hasHandles: true,
            label: "Multi-Agent",
            immobile: true,
            style: {
              // arbitrary CSS styling for your bar
              background: "#5f9ea0",
              borderRadius: "20px",
              color: "black",
              fontSize: "10px"

            }
          }
        }
      ]
    },
    {
      title: "STUN/TURN Service",
      bars: [
        {
          myBeginDate: "2025-06-01",
          myEndDate: "2025-07-07",
          ganttBarConfig: {
            id: "STUN/TURNService-1",
            hasHandles: true,
            label: "Multi-Agent",
            immobile: true,
            style: {
              // arbitrary CSS styling for your bar
              background: "#5f9ea0",
              borderRadius: "20px",
              color: "black",
              fontSize: "10px"

            }
          }
        }
      ]
    },
    {
      title: "Project Webpage",
      bars: [
        {
          myBeginDate: "2025-03-01",
          myEndDate: "2025-05-05",
          ganttBarConfig: {
            id: "Webpage-1",
            hasHandles: true,
            label: "Start a Webpage in github and init in HKUCS",
            immobile: true,
            style: {
              // arbitrary CSS styling for your bar
              background: "#5f9ea0",
              borderRadius: "20px",
              color: "black",
              fontSize: "10px"

            }
          }
        },
        {
          myBeginDate: "2025-05-06",
          myEndDate: "2025-07-15",
          ganttBarConfig: {
            id: "Webpage-1",
            hasHandles: true,
            label: "Update a Webpage in HKUCS",
            immobile: true,
            style: {
              // arbitrary CSS styling for your bar
              background: "#5f9ea0",
              borderRadius: "20px",
              color: "black",
              fontSize: "10px"

            }
          }
        }
      ]
    },
    {
      title: "Final Report",
      bars: [
        {
          myBeginDate: "2025-06-18",
          myEndDate: "2025-07-18",
          ganttBarConfig: {
            id: "report-1",
            hasHandles: true,
            label: "Final Report",
            immobile: true,
            style: {
              // arbitrary CSS styling for your bar
              background: "#5f9ea0",
              borderRadius: "20px",
              color: "black",
              fontSize: "10px"
            }
          }
        }
      ]
    },
  ]
)

onMounted(() => {
  ganttChartRowHeight.value = (ganttChartRef.value.getBoundingClientRect().height - 80) / rowBarList.value.length
  onresize = () => {
    if (ganttChartRef.value) {
      ganttChartRowHeight.value = (ganttChartRef.value.getBoundingClientRect().height - 80) / rowBarList.value.length
    }
  }
})

</script>
<style lang="scss" scoped>
.gantt-chart {
  width: 100%;
  height: calc(100%);
  margin: 0px 0px 0px 0;
}

</style>
<template>
  <div class="conference-records">
    <Card v-for="conference in conferences" class="conference-record" :key="conference.name">
      <template #header>
        <div class="title">
          <FontAwesomeIcon :icon="fas.faVideo" />
          <div>Meeting Record</div>
        </div>
      </template>
      <template #content>
        <div class="conference-content">
          <div class="text">
            <p>{{ conference.name }}</p>
            <p>{{ conference.date }} {{ conference.time }}</p>
          </div>

        </div>
      </template>
      <template #footer>
        <div class="conference-footer">
          <AvatarGroup>
            <Avatar v-for="participant in conference.participants" :key="participant" shape="circle"
              :label="participant.toString()"></Avatar>
          </AvatarGroup>
          <Button severity="info" class="toolbar-button" @click="redirect(conference.records)">
            <FontAwesomeIcon :icon="fas.faVideo" />
            Play
          </Button>
        </div>
      </template>
    </Card>
  </div>
</template>

<script setup lang="ts">
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { fas } from '@fortawesome/free-solid-svg-icons';
import { Card, Avatar, AvatarGroup, Button } from 'primevue';
import { ref } from 'vue';
import { router } from '@/router';

const conferences = ref([
  {
    name: 'Conference 1',
    date: '2023-09-10',
    time: '10:00',
    participants: [11, 22, 33],
    records: '11'
  },
  {
    name: 'Conference 2',
    date: '2024-09-10',
    time: '11:00',
    participants: [11, 99, 33],
    records: '13'
  },
  {
    name: 'COMP7506 meeting',
    date: '2023-09-10',
    time: '13:00',
    participants: [44, 33, 77],
    records: '12'
  },
])
const redirect = (id: string) => {
  router.push({ path: `/home/conference-record/${id}` });
}

</script>

<style scoped lang="scss">
.conference-records {
  height: 100%;
  width: 100%;
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  overflow: auto;

  .conference-record {
    width: 300px;
    height: 200px;
    background: #151e34;
    box-shadow: 0px 4px 4px rgba(0, 0, 0, 0.25);
    border-radius: 10px;
    padding: 20px 20px 0 20px;
    margin: 10px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;

    .p-card-body{
      padding: 0 !important;
    }

    .title{
      display: flex;  
      justify-content: space-between;
      font-weight: 900;
    }
    .conference-content {
      display: flex;
      justify-content: space-between;
      p {
        text-align: start;        
        margin: 0;
      }
    }
    .conference-footer{
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
  }
}
</style>
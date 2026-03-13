<template>
  <div>

    <OrgNavbar />

    <h1>Мои хакатоны</h1>

    <NuxtLink to="/org/hackathon/add">
      <button>Добавить хакатон</button>
    </NuxtLink>

    <table>

      <thead>
        <tr>
          <th>Название</th>
          <th>Тематика</th>
          <th>Формат</th>
        </tr>
      </thead>

      <tbody>

        <tr
          v-for="hackathon in hackathons"
          :key="hackathon.id"
          @click="goToHackathon(hackathon.id)"
        >
          <td>{{ hackathon.name }}</td>
          <td>{{ hackathon.theme }}</td>
          <td>{{ hackathon.format }}</td>
        </tr>

      </tbody>

    </table>

  </div>
</template>

<script setup lang="ts">

import { useHackathonStore } from "~/stores/hackathonStore"
import OrgNavbar from "~/components/OrgNavbar.vue"

const store = useHackathonStore()

const hackathons = store.getOrganizerHackathons("1")

const router = useRouter()

function goToHackathon(id: string) {
  router.push(`/org/hackathon/${id}`)
}

</script>
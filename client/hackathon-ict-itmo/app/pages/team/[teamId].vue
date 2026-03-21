<template>
  <div>
    <Card>
      <h1>{{ team?.name || "Загрузка..." }}</h1>

      <div v-if="team">
        <p>Капитан: {{ team.members.find(el => el.id === team?.captainId)?.name }}</p>

        <h3>Участники</h3>
        <ul>
          <li v-for="m in team.members" :key="m.id" class="member-row">
            <div class="member-info">
              <span class="member-name">{{ m.name }}</span>
              <span v-if="m.id === team.captainId" class="member-role">(капитан)</span>
            </div>

            <div class="member-actions">
              <Button
                variant="secondary"
                :disabled="excludingMemberId === m.id"
                @click="excludeMember(m.id)"
              >
                Исключить
              </Button>

              <Button
                variant="primary"
                :disabled="m.id === team.captainId || settingCaptainId === m.id"
                style="margin-left: 0.5rem;"
                @click="setCaptain(m.id)"
              >
                Назначить капитана
              </Button>
            </div>
          </li>
        </ul>

        <Button @click="submitJoin" variant="primary" :disabled="submittingJoin" style="margin-right: 1rem;">
          Подать заявку в команду
        </Button>
        <Button @click="apply" variant="primary">
          Подать заявку на хакатон
        </Button>
      </div>
    </Card>

    <Card>
      <h2>Заявки на вступление</h2>

      <table>
        <thead>
          <tr>
            <th>Пользователь</th>
            <th>Статус</th>
            <th></th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="r in joinRequests" :key="r.id">
            <td>{{ r.userName || r.userId || "—" }}</td>
            <td>{{ r.status }}</td>
            <td>
              <button @click="approve(r.id)">Одобрить</button>
            </td>
            <td>
              <button @click="reject(r.id)">Отклонить</button>
            </td>
          </tr>
        </tbody>
      </table>
    </Card>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from "vue"
import { useRoute, useRouter } from "vue-router"
import Card from "~/components/ui/Card.vue"
import Button from "~/components/ui/Button.vue"
import { useTeamStore } from "~/stores/teamStore"

const route = useRoute()
const store = useTeamStore()

const teamId = computed(() => route.params.teamId as string)

const team = computed(() => store.getTeamById(teamId.value))
const joinRequests = computed(() => store.getJoinRequests(teamId.value))

const submittingJoin = ref(false)
const excludingMemberId = ref<string | null>(null)
const settingCaptainId = ref<string | null>(null)

onMounted(async () => {
  try {
    await store.fetchTeam(teamId.value)
    await store.fetchJoinRequests(teamId.value)
  } catch (e) {
    console.error(e)
    alert("Вам не доступен просмотр заявок команды, так как вы не капитан!")
  }
})

const router = useRouter()

function apply() {
  router.push({ path: "/hackathons/apply", query: { teamId: teamId.value } })
}

async function excludeMember(userId: string) {
  if (excludingMemberId.value) return
  const ok = window.confirm("Исключить участника из команды?")
  if (!ok) return

  excludingMemberId.value = userId
  try {
    await store.excludeMember(teamId.value, userId)
    alert("Участник исключен")
  } catch (e) {
    console.error(e)
    alert("Не удалось исключить участника")
  } finally {
    excludingMemberId.value = null
  }
}

async function setCaptain(userId: string) {
  console.log(settingCaptainId.value)
  if (settingCaptainId.value) return
  settingCaptainId.value = userId

  try {
    await store.setCaptain(teamId.value, userId)
    alert("Капитан назначен")
  } catch (e) {
    console.error(e)
    alert("Не удалось назначить капитана")
  } finally {
    settingCaptainId.value = null
  }
}

async function submitJoin() {
  submittingJoin.value = true
  try {
    await store.submitJoinRequest(teamId.value)
    alert("Заявка отправлена")
  } catch (e) {
    console.error(e)
    alert("Не удалось отправить заявку")
  } finally {
    submittingJoin.value = false
  }
}

async function approve(requestId: string) {
  try {
    await store.approveJoinRequest(requestId, teamId.value)
    alert("Заявка одобрена")
    await store.fetchTeam(teamId.value)
  } catch (e) {
    console.error(e)
    alert("Не удалось одобрить заявку")
  }
}

async function reject(requestId: string) {
  try {
    await store.rejectJoinRequest(requestId, teamId.value)
    alert("Заявка отклонена")
    await store.fetchTeam(teamId.value)
  } catch (e) {
    console.error(e)
    alert("Не удалось отклонить заявку")
  }
}
</script>

<style scoped>
.member-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  margin-bottom: 0.5rem;
}

.member-info {
  display: flex;
  align-items: baseline;
  gap: 0.5rem;
}

.member-role {
  color: var(--color-primary);
  font-style: normal;
}

.member-actions {
  display: flex;
  align-items: center;
}
</style>

<template>
  <div class="container mt-5">
      <div>
          <table class="table">
              <thead>
                  <tr>
                      <th scope="col">CID</th>
                      <th scope="col">Name</th>
                      <th scope="col">Prerequisite</th>
                      <th scope="col">Trainer</th>
                  </tr>
              </thead>

              <tbody v-for="course in courses" :key="course.CID">
                  <tr>
                      <th scope="row">{{course.CID}}</th>
                      <th scope="row">{{course.name}}</th>
                      <th scope="row">{{course.prerequisites}}</th>
                      <th scope="row">{{course.trainers}}</th>
                  </tr>
              </tbody>
          </table>
      </div>
  </div>
</template>

<script>
export default {

    data() {
        return {
            courses:[],
        }
    },

    methods: {
        getCourses() {
            fetch('http://localhost:5001/view_courses', {
                method: "GET",
                headers: {
                    "Content-Type" : "application/json"
                }
            })
            .then(resp => resp.json())
            .then(data => {
                this.courses.push(...data.data)
                
            })
            .catch(error => {
                console.log(error)
            })
        }
    },
    created() {
        this.getCourses()
    }
}
</script>

<style>

</style>
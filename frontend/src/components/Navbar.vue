<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light">
  <div class="container-fluid">
    
	<router-link class="navbar-brand" to="/">Flask & Vue</router-link>
    
    <div class="collapse navbar-collapse" id="navbarNav">
      <ul class="navbar-nav">
        <li class="nav-item">
          <router-link class="btn btn-primary mx-2" aria-current="page" to="/">Home</router-link>
        </li>

        <li class="nav-item">
          <router-link class="btn btn-success" to="/create">Pricing</router-link>
        </li>
      </ul>
    </div>
  </div>
  </nav>
</template>

<script>
export default {

}
</script>

<style>

</style>
---
layout: page
title: AL Adventures
datatable: true
---

{% assign dc_adventures = site.data.SJ-DC %}

<div class="datatable-begin">
<table class="sortable">
  <thead>
    <tr>
      <th>Code</th>
      <th>Title</th>
      <th>Authors</th>
      <th>URL</th>
    </tr>
  </thead>
  <tbody>
    {% for item in dc_adventures %}
      <tr>
        <td>{{ item.code }}</td>
        <td>{{ item.title }}</td>
        <td>{{ item.authors | join: ", " }}</td>
        <td><a href="{{ item.url }}">{{ item.url }}</a></td>
      </tr>
    {% endfor %}
  </tbody>
</table>

</div>

<link href="https://cdn.jsdelivr.net/gh/tofsjonas/sortable@latest/sortable.min.css" rel="stylesheet" />
<script src="https://cdn.jsdelivr.net/gh/tofsjonas/sortable@latest/sortable.min.js"></script>
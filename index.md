---
layout: page
title: AL Adventures
---

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
    {% for item in site.data.SJ-DC %}
      <tr>
        <td>{{ item.code }}</td>
        <td>{{ item.title }}</td>
        <td>{{ item.authors | join: ", " }}</td>
        <td><a href="{{ item.url }}">{{ item.url }}</a></td>
      </tr>
    {% endfor %}
  </tbody>
</table>

<link href="https://cdn.jsdelivr.net/gh/tofsjonas/sortable@latest/sortable.min.css" rel="stylesheet" />
<script src="https://cdn.jsdelivr.net/gh/tofsjonas/sortable@latest/sortable.min.js"></script>
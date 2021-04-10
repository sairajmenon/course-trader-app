import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { ChatComponent } from './chat/chat.component';
import { ForumComponentComponent } from './forum-component/forum-component.component';
import { LoginComponentComponent } from './login-component/login-component.component';
import { CourseTraderComponent } from './course-trader/course-trader.component';

@NgModule({
  declarations: [
    AppComponent,
    ChatComponent,
    ForumComponentComponent,
    LoginComponentComponent,
    CourseTraderComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
